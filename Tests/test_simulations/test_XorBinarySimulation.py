import numpy as np

from savageml.simulations import SimulationState
from savageml.simulations import BinaryXorSimulation


def test_initial_state_initialized():
    simulation = BinaryXorSimulation()
    assert simulation.get_state() == SimulationState.INITIALIZED


def test_state_after_run_completed():
    simulation = BinaryXorSimulation()
    simulation.run()
    assert simulation.get_state() == SimulationState.COMPLETE


def test_state_after_step_not_initialized():
    simulation = BinaryXorSimulation()
    simulation.step()
    assert simulation.get_state() != SimulationState.INITIALIZED


def test_reset_state_initialized():
    simulation = BinaryXorSimulation()
    simulation.step()
    simulation.reset()
    assert simulation.get_state() == SimulationState.INITIALIZED


def test_simulation_duplicates():
    simulation = BinaryXorSimulation(seed=1)
    simulation_duplicate = simulation.__iter__()
    assert simulation.get_seed() == simulation_duplicate.get_seed()
    assert all(np.all(val == dup_val) for val, dup_val in zip(simulation.step(), simulation_duplicate.step()))


def test_simulation_shape_correct():
    test_shape = (5, 7)
    expected_test_shape = (1, 5, 7)
    expected_out_shape = (1, 1)
    simulation = BinaryXorSimulation(seed=1, shape=test_shape)
    result = simulation.step()
    assert result[0].shape == expected_test_shape
    assert result[1].shape == expected_out_shape


def test_xor_simulation_all_true():
    test_shape = (2, 2)
    all_ones_seeds = 4
    simulation = BinaryXorSimulation(seed=all_ones_seeds, shape=test_shape)
    result = simulation.step()
    assert (result[0] == 1.0).all()
    assert (result[1] == 0.0).all()


def test_xor_simulation_all_false():
    test_shape = (2, 2)
    all_zero_seeds = 36
    simulation = BinaryXorSimulation(seed=all_zero_seeds, shape=test_shape)
    result = simulation.step()
    assert (result[0] == 0.0).all()
    assert (result[1] == 0.0).all()


def test_xor_simulation_50_50():
    test_shape = (2, 2)
    _50_50_seeds = 31
    simulation = BinaryXorSimulation(seed=_50_50_seeds, shape=test_shape)
    result = simulation.step()
    assert (result[0] == 1.0).sum() == (result[0] == 0.0).sum()
    assert (result[1] == 0.0).all()


def test_xor_simulation_just_one_true():
    test_shape = (2, 2)
    _50_50_seeds = 2
    simulation = BinaryXorSimulation(seed=_50_50_seeds, shape=test_shape)
    result = simulation.step()
    assert (result[0] == 1.0).sum() == 1
    assert (result[1] == 1.0).all()


def test_simulation_step_count():
    max_steps = 11
    simulation = BinaryXorSimulation(seed=1, max_steps=max_steps)
    count = 0
    for _ in simulation:
        count += 1
    assert count == max_steps
    simulation.reset()
    assert simulation.get_state() == SimulationState.INITIALIZED
    for _ in range(max_steps):
        simulation.step()
    assert simulation.get_state() == SimulationState.COMPLETE
