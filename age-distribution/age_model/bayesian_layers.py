"""
Contains priors for the bayesian networks.
"""
import tensorflow as tf
import tensorflow_probability as tfp


def approximate_kl(q, p, q_tensor):
    return tf.reduce_mean(q.log_prob(q_tensor) - p.log_prob(q_tensor))


def divergence_fn(q, p, q_tensor):
    total_samples = 60000
    return approximate_kl(q, p, q_tensor) / total_samples


def custom_mvn_prior(dtype, shape):
    distribution = tfp.distributions.Normal(loc=0.1 * tf.ones(shape, dtype),
                                            scale=0.003 * tf.ones(shape, dtype))
    batch_ndims = tf.size(distribution.batch_shape_tensor())

    independent_distribution = tfp.distributions.Independent(distribution,
                                                             reinterpreted_batch_ndims=batch_ndims)
    return independent_distribution


def conv_reparameterization_layer(filters, kernel_size, activation, strides=(1, 1),
                                  padding="same"):
    # For simplicity, we use default prior and posterior.
    # In the next parts, we will use custom mixture prior and posteriors.
    return tfp.layers.Convolution2DReparameterization(
        filters=filters,
        strides=strides,
        kernel_size=kernel_size,
        activation=activation,
        padding=padding,
        kernel_posterior_fn=tfp.layers.default_mean_field_normal_fn(is_singular=False),
        kernel_prior_fn=tfp.layers.default_multivariate_normal_fn,

        bias_prior_fn=tfp.layers.default_multivariate_normal_fn,
        bias_posterior_fn=tfp.layers.default_mean_field_normal_fn(is_singular=False),

        kernel_divergence_fn=divergence_fn,
        bias_divergence_fn=divergence_fn,
    )


def dense_reparametrization_layer(n_classes):
    return tfp.layers.DenseReparameterization(
        units=tfp.layers.OneHotCategorical.params_size(n_classes), activation=None,
        kernel_posterior_fn=tfp.layers.default_mean_field_normal_fn(is_singular=False),
        kernel_prior_fn=tfp.layers.default_multivariate_normal_fn,

        bias_prior_fn=tfp.layers.default_multivariate_normal_fn,
        bias_posterior_fn=tfp.layers.default_mean_field_normal_fn(is_singular=False),

        kernel_divergence_fn=divergence_fn,
        bias_divergence_fn=divergence_fn)
