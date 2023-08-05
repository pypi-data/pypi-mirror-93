import os
import sys

import numpy as np
import pytest

skip_on_win_ci = pytest.mark.skipif(
    sys.platform.startswith('win') and os.getenv('CI', '0') != '0',
    reason='Screenshot tests are not supported on windows CI.',
)
skip_local_popups = pytest.mark.skipif(
    not os.getenv('CI') and os.getenv('NAPARI_POPUP_TESTS', '0') == '0',
    reason='Tests requiring GUI windows are skipped locally by default.',
)


def test_multiscale(make_napari_viewer):
    """Test rendering of multiscale data."""
    viewer = make_napari_viewer()

    shapes = [(4000, 3000), (2000, 1500), (1000, 750), (500, 375)]
    np.random.seed(0)
    data = [np.random.random(s) for s in shapes]
    _ = viewer.add_image(data, multiscale=True, contrast_limits=[0, 1])
    layer = viewer.layers[0]

    # Set canvas size to target amount
    viewer.window.qt_viewer.view.canvas.size = (800, 600)
    viewer.window.qt_viewer.on_draw(None)

    # Check that current level is first large enough to fill the canvas with
    # a greater than one pixel depth
    assert layer.data_level == 2

    # Check that full field of view is currently requested
    assert np.all(layer.corner_pixels[0] <= [0, 0])
    assert np.all(layer.corner_pixels[1] >= np.subtract(shapes[2], 1))

    # Test value at top left corner of image
    viewer.cursor.position = (0, 0)
    value = layer.get_value(layer.coordinates)
    np.testing.assert_allclose(value, (2, data[2][(0, 0)]))

    # Test value at bottom right corner of image
    viewer.cursor.position = (3995, 2995)
    value = layer.get_value(layer.coordinates)
    np.testing.assert_allclose(value, (2, data[2][(999, 749)]))

    # Test value outside image
    viewer.cursor.position = (4000, 3000)
    value = layer.get_value(layer.coordinates)
    assert value[1] is None


def test_3D_multiscale_image(make_napari_viewer):
    """Test rendering of 3D multiscale image uses lowest resolution."""
    viewer = make_napari_viewer()

    data = [np.random.random((128,) * 3), np.random.random((64,) * 3)]
    viewer.add_image(data)

    # Check that this doesn't crash.
    viewer.dims.ndisplay = 3

    # Check lowest resolution is used
    assert viewer.layers[0].data_level == 1

    # Note that draw command must be explicitly triggered in our tests
    viewer.window.qt_viewer.on_draw(None)


@skip_on_win_ci
@skip_local_popups
def test_multiscale_screenshot(make_napari_viewer):
    """Test rendering of multiscale data with screenshot."""
    viewer = make_napari_viewer(show=True)

    shapes = [(4000, 3000), (2000, 1500), (1000, 750), (500, 375)]
    data = [np.ones(s) for s in shapes]
    _ = viewer.add_image(data, multiscale=True, contrast_limits=[0, 1])

    # Set canvas size to target amount
    viewer.window.qt_viewer.view.canvas.size = (800, 600)

    screenshot = viewer.screenshot(canvas_only=True)
    center_coord = np.round(np.array(screenshot.shape[:2]) / 2).astype(np.int)
    target_center = np.array([255, 255, 255, 255], dtype='uint8')
    target_edge = np.array([0, 0, 0, 255], dtype='uint8')
    screen_offset = 3  # Offset is needed as our screenshots have black borders

    np.testing.assert_allclose(screenshot[tuple(center_coord)], target_center)
    np.testing.assert_allclose(
        screenshot[screen_offset, screen_offset], target_edge
    )
    np.testing.assert_allclose(
        screenshot[-screen_offset, -screen_offset], target_edge
    )


@skip_on_win_ci
@skip_local_popups
def test_multiscale_screenshot_zoomed(make_napari_viewer):
    """Test rendering of multiscale data with screenshot after zoom."""
    viewer = make_napari_viewer(show=True)
    view = viewer.window.qt_viewer

    shapes = [(4000, 3000), (2000, 1500), (1000, 750), (500, 375)]
    data = [np.ones(s) for s in shapes]
    _ = viewer.add_image(data, multiscale=True, contrast_limits=[0, 1])

    # Set canvas size to target amount
    view.view.canvas.size = (800, 600)

    # Set zoom of camera to show highest resolution tile
    view.view.camera.rect = [1000, 1000, 200, 150]
    viewer.window.qt_viewer.on_draw(None)

    # Check that current level is bottom level of multiscale
    assert viewer.layers[0].data_level == 0

    screenshot = viewer.screenshot(canvas_only=True)
    center_coord = np.round(np.array(screenshot.shape[:2]) / 2).astype(np.int)
    target_center = np.array([255, 255, 255, 255], dtype='uint8')
    screen_offset = 3  # Offset is needed as our screenshots have black borders

    np.testing.assert_allclose(screenshot[tuple(center_coord)], target_center)
    np.testing.assert_allclose(
        screenshot[screen_offset, screen_offset], target_center
    )
    np.testing.assert_allclose(
        screenshot[-screen_offset, -screen_offset], target_center
    )


@skip_on_win_ci
@skip_local_popups
def test_image_screenshot_zoomed(make_napari_viewer):
    """Test rendering of image data with screenshot after zoom."""
    viewer = make_napari_viewer(show=True)
    view = viewer.window.qt_viewer

    data = np.ones((4000, 3000))
    _ = viewer.add_image(data, multiscale=False, contrast_limits=[0, 1])

    # Set canvas size to target amount
    view.view.canvas.size = (800, 600)

    # Set zoom of camera to show highest resolution tile
    view.view.camera.rect = [1000, 1000, 200, 150]
    viewer.window.qt_viewer.on_draw(None)

    screenshot = viewer.screenshot(canvas_only=True)
    center_coord = np.round(np.array(screenshot.shape[:2]) / 2).astype(np.int)
    target_center = np.array([255, 255, 255, 255], dtype='uint8')
    screen_offset = 3  # Offset is needed as our screenshots have black borders

    np.testing.assert_allclose(screenshot[tuple(center_coord)], target_center)
    np.testing.assert_allclose(
        screenshot[screen_offset, screen_offset], target_center
    )
    np.testing.assert_allclose(
        screenshot[-screen_offset, -screen_offset], target_center
    )


@skip_on_win_ci
@skip_local_popups
def test_5D_multiscale(make_napari_viewer):
    """Test 5D multiscale data."""
    # Show must be true to trigger multiscale draw and corner estimation
    viewer = make_napari_viewer(show=True)
    shapes = [(1, 2, 5, 20, 20), (1, 2, 5, 10, 10), (1, 2, 5, 5, 5)]
    np.random.seed(0)
    data = [np.random.random(s) for s in shapes]
    layer = viewer.add_image(data, multiscale=True)
    assert layer.data == data
    assert layer.multiscale is True
    assert layer.ndim == len(shapes[0])
