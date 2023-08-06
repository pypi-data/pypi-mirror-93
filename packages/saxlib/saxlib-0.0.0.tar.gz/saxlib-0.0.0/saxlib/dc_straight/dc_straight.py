import os
import json

import jax
import jax.numpy as jnp

CURDIR = os.path.abspath(os.path.dirname(__file__))
WEIGHTDIR = os.path.join(CURDIR, "weights")
os.makedirs(WEIGHTDIR, exist_ok=True)


def _load_json_weights(filename, default=None):
    if not os.path.exists(filename):
        return {} if default is None else dict(default)
    with open(filename, "r") as file:
        weights = {k: jnp.array(v) for k, v in json.load(file).items()}
    return weights


neff_norms = _load_json_weights(
    filename=os.path.join(WEIGHTDIR, "neff_norms.json"),
    default={"x_mean": 0.0, "x_std": 1.0, "y_mean": 0.0, "y_std": 1.0},
)


def save_neff_weights(weights, filename=None):
    if filename is None:
        L = len(weights) // 2
        H = weights["win"].shape[-1]  # number of neurons per layer
        filename = os.path.join(
            WEIGHTDIR, f"neff_weights_L={str(L).zfill(2)}_H={str(H).zfill(3)}.json"
        )
    with open(filename, "w") as file:
        json.dump({k: v.tolist() for k, v in weights.items()}, file)


def load_neff_weights(L, H):
    filename = os.path.join(
        WEIGHTDIR, f"neff_weights_L={str(L).zfill(2)}_H={str(H).zfill(3)}.json"
    )
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"No weights for neural networks with {L} layers and {H} neurons "
            f"per layers found.\nfile not found: '{filename}'"
        )
    return _load_json_weights(filename)


def load_neff_model(L):
    g = globals()
    funcname = f"dc_neff_fcnn{str(L).zfill(2)}"
    if funcname not in g:
        raise NameError(f"neff model '{funcname}' not found")
    func = g[funcname]
    return func


def generate_random_weights(L, H, key=42):
    if isinstance(key, int):
        key = jax.random.PRNGKey(key)
    [key, *keys] = jax.random.split(key, 1 + 2 * L)
    rand = jax.nn.initializers.lecun_normal()
    weights = {}
    weights["win"] = rand(keys[0], (52, H)) # 52: number of preprocessed dimensions
    weights["bin"] = rand(keys[1], (1, H))
    for i in range(1, L - 1):
        weights[f"w{str(i).zfill(2)}"] = rand(keys[2 * i], (H, H))
        weights[f"b{str(i).zfill(2)}"] = rand(keys[2 * i + 1], (1, H))
    weights["wout"] = rand(keys[(L - 1) * 2], (H, 2))
    weights["bout"] = rand(keys[(L - 1) * 2 + 1], (1, 2))
    return weights, key


def dc_preprocess(
    wl,
    dc_gap,
    wg_width,
    wg_height,
    wg_sw_angle,
):
    (
        wl,
        dc_gap,
        wg_width,
        wg_height,
        wg_sw_angle,
    ) = jnp.broadcast_arrays(
        wl,
        dc_gap,
        wg_width,
        wg_height,
        wg_sw_angle,
    )
    wg_sw_angle = wg_sw_angle * jnp.pi / 180
    wg_sw_sin = jnp.sin(wg_sw_angle)
    wg_sw_cos = jnp.cos(wg_sw_angle)
    wg_sw_length = wg_height / wg_sw_sin
    wg_width_btm = wg_width + 2 * wg_sw_length * wg_sw_cos
    dc_gap_btm = dc_gap - 2 * wg_sw_length * wg_sw_cos
    x = jnp.stack(
        [
            wg_sw_angle,
            wg_sw_sin,
            wg_sw_cos,
            wl * 1e6,
            wl / wg_width,
            wl / wg_width_btm,
            wl / wg_height,
            wl / wg_sw_length,
            wl / dc_gap,
            wl / dc_gap_btm,
            wg_width * 1e6,
            wg_width / wl,
            wg_width / wg_width_btm,
            wg_width / wg_height,
            wg_width / wg_sw_length,
            wg_width / dc_gap,
            wg_width / dc_gap_btm,
            wg_width_btm * 1e6,
            wg_width_btm / wl,
            wg_width_btm / wg_width,
            wg_width_btm / wg_height,
            wg_width_btm / wg_sw_length,
            wg_width_btm / dc_gap,
            wg_width_btm / dc_gap_btm,
            wg_height * 1e6,
            wg_height / wl,
            wg_height / wg_width,
            wg_height / wg_width_btm,
            wg_height / wg_sw_length,
            wg_height / dc_gap,
            wg_height / dc_gap_btm,
            wg_sw_length * 1e6,
            wg_sw_length / wl,
            wg_sw_length / wg_width,
            wg_sw_length / wg_width_btm,
            wg_sw_length / wg_height,
            wg_sw_length / dc_gap,
            wg_sw_length / dc_gap_btm,
            dc_gap * 1e6,
            dc_gap / wl,
            dc_gap / wg_width,
            dc_gap / wg_width_btm,
            dc_gap / wg_height,
            dc_gap / wg_sw_length,
            dc_gap / dc_gap_btm,
            dc_gap_btm * 1e6,
            dc_gap_btm / wl,
            dc_gap_btm / wg_width,
            dc_gap_btm / wg_width_btm,
            dc_gap_btm / wg_height,
            dc_gap_btm / wg_sw_length,
            dc_gap_btm / dc_gap,
        ],
        -1,
    )
    return x


def dc_neff_fcnn02(
    weights,
    wl,
    dc_gap,
    wg_width,
    wg_height,
    wg_sw_angle,
):
    """2-layer fully connected neural network predicting dc_rib neff

    Args:
        weights: the neural network weights dictionary
        wl: the wavelength(s)
        dc_gap: the direciontal coupler gap(s)
        wg_width: waveguide width
        wg_height: waveguide height 
        wg_sw_angle: waveguide sidewall angle (degrees)

    """
    x = dc_preprocess(
        wl,
        dc_gap,
        wg_width,
        wg_height,
        wg_sw_angle,
    )
    x = (x - neff_norms["x_mean"]) / neff_norms["x_std"]
    x = jax.nn.leaky_relu(x @ weights["win"] + weights["bin"])
    x = x @ weights["wout"] + weights["bout"]
    x = x.reshape(-1, 2) * neff_norms["y_std"] + neff_norms["y_mean"]
    return x