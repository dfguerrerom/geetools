"""Test the ``Image`` class."""
import ee
import pytest

import geetools


class TestAddDate:
    """Test the ``addDate`` method."""

    def test_add_date(self, image_instance, vatican):
        image = image_instance.geetools.addDate()
        dateBand = image.select("date")
        date = dateBand.reduceRegion(ee.Reducer.first(), vatican, 10).get("date")
        assert image.bandNames().size().getInfo() > 1
        assert ee.Date(date).format("YYYY-MM-DD").getInfo() == "2020-01-01"

    def test_deprecated_method(self, image_instance, vatican):
        with pytest.deprecated_call():
            image = geetools.tools.date.makeDateBand(image_instance)
            dateBand = image.select("date")
            date = dateBand.reduceRegion(ee.Reducer.first(), vatican, 10).get("date")
            assert image.bandNames().size().getInfo() > 1
            assert ee.Date(date).format("YYYY-MM-DD").getInfo() == "2020-01-01"

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        return ee.Image(
            "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        )

    @pytest.fixture
    def vatican(self):
        """A 10 m buffer around the Vatican."""
        return ee.Geometry.Point([12.4534, 41.9033]).buffer(100)


class TestAddSuffix:
    """Test the ``addSuffix`` method."""

    def test_add_suffix_to_all(self, image_instance):
        image = image_instance.geetools.addSuffix("_suffix")
        assert image.bandNames().size().getInfo() > 1
        assert image.bandNames().getInfo() == [
            "B1_suffix",
            "B2_suffix",
            "B3_suffix",
        ]

    def test_add_suffix_to_selected(self, image_instance):
        image = image_instance.geetools.addSuffix("_suffix", bands=["B1", "B2"])
        assert image.bandNames().size().getInfo() > 1
        assert image.bandNames().getInfo() == ["B1_suffix", "B2_suffix", "B3"]

    def test_deprecated_method(self, image_instance):
        with pytest.deprecated_call():
            image = geetools.tools.image.addSuffix(
                image_instance, "_suffix", ["B1", "B2"]
            )
            assert image.bandNames().getInfo() == ["B1_suffix", "B2_suffix", "B3"]

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        src = "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        return ee.Image(src).select(["B1", "B2", "B3"])


class TestAddPrefix:
    """Test the ``addPrefix`` method."""

    def test_add_prefix_to_all(self, image_instance):
        image = image_instance.geetools.addPrefix("prefix_")
        assert image.bandNames().size().getInfo() > 1
        assert image.bandNames().getInfo() == [
            "prefix_B1",
            "prefix_B2",
            "prefix_B3",
        ]

    def test_add_prefix_to_selected(self, image_instance):
        image = image_instance.geetools.addPrefix("prefix_", bands=["B1", "B2"])
        assert image.bandNames().size().getInfo() > 1
        assert image.bandNames().getInfo() == ["prefix_B1", "prefix_B2", "B3"]

    def test_deprecated_method(self, image_instance):
        with pytest.deprecated_call():
            image = geetools.tools.image.addPrefix(
                image_instance, "prefix_", ["B1", "B2"]
            )
            assert image.bandNames().getInfo() == ["prefix_B1", "prefix_B2", "B3"]

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        src = "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        return ee.Image(src).select(["B1", "B2", "B3"])


class TestGetValues:
    """Test the ``getValues`` method."""

    def test_get_values(self, image_instance, vatican):
        values = image_instance.geetools.getValues(vatican)
        assert values.getInfo() == {"B1": 218, "B2": 244, "B3": 251}

    def test_get_values_with_scale(self, image_instance, vatican):
        values = image_instance.geetools.getValues(vatican, scale=100)
        assert values.getInfo() == {"B1": 117, "B2": 161, "B3": 247}

    def test_deprecated_method(self, image_instance, vatican):
        with pytest.deprecated_call():
            values = geetools.tools.image.getValue(image_instance, vatican)
            assert values.getInfo() == {"B1": 218, "B2": 244, "B3": 251}

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        src = "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        return ee.Image(src).select(["B1", "B2", "B3"])

    @pytest.fixture
    def vatican(self):
        """Return a vatican in the Vatican."""
        return ee.Geometry.Point([12.4534, 41.9029])


class TestMinScale:
    """Test the ``minScale`` method."""

    def test_min_scale(self, image_instance):
        scale = image_instance.geetools.minScale()
        assert scale.getInfo() == 10

    def test_deprecated_method(self, image_instance):
        with pytest.deprecated_call():
            scale = geetools.tools.image.minscale(image_instance)
            assert scale.getInfo() == 10

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        src = "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        return ee.Image(src).select(["B1", "B2", "B3"])


class TestMerge:
    """Test the ``merge`` method."""

    def test_merge(self, image_instance):
        image = image_instance.geetools.merge([image_instance, image_instance])
        assert image.bandNames().getInfo() == [
            "B1",
            "B2",
            "B1_1",
            "B2_1",
            "B1_2",
            "B2_2",
        ]

    def test_deprecated_method(self, image_instance):
        with pytest.deprecated_call():
            image = geetools.tools.image.addMultiBands([image_instance, image_instance])
            assert image.bandNames().getInfo() == ["B1", "B2", "B1_1", "B2_1"]

    def test_deprecated_method2(self, image_instance):
        with pytest.deprecated_call():
            image = geetools.tools.image.mixBands([image_instance, image_instance])
            assert image.bandNames().getInfo() == ["B1", "B2", "B1_1", "B2_1"]

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        src = "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        return ee.Image(src).select(["B1", "B2"])


class TestRename:
    """Test the ``rename`` method."""

    def test_rename(self, image_instance):
        image = image_instance.geetools.rename({"B1": "newB1", "B2": "newB2"})
        assert image.bandNames().getInfo() == ["newB1", "newB2", "B3"]

    def test_deprecated_method(self, image_instance):
        with pytest.deprecated_call():
            image = geetools.tools.image.renameDict(
                image_instance, {"B1": "newB1", "B2": "newB2"}
            )
            assert image.bandNames().getInfo() == ["newB1", "newB2", "B3"]

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        src = "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        return ee.Image(src).select(["B1", "B2", "B3"])


class TestRemove:
    """Test the ``remove`` method."""

    def test_remove(self, image_instance):
        image = image_instance.geetools.remove(["B1", "B2"])
        assert image.bandNames().getInfo() == ["B3"]

    def test_deprecated_method(self, image_instance):
        with pytest.deprecated_call():
            image = geetools.tools.image.removeBands(image_instance, ["B1", "B2"])
            assert image.bandNames().getInfo() == ["B3"]

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        src = "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        return ee.Image(src).select(["B1", "B2", "B3"])


class TestToGrid:
    """Test the ``toGrid`` method."""

    def test_to_grid(self, image_instance, vatican, data_regression):
        grid = image_instance.geetools.toGrid(1, "B2", vatican)
        data_regression.check(grid.getInfo())

    def test_deprecated_method(self, image_instance, vatican, data_regression):
        with pytest.deprecated_call():
            grid = geetools.tools.image.toGrid(image_instance, 1, "B2", vatican)
            data_regression.check(grid.getInfo())

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        src = "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        return ee.Image(src).select(["B1", "B2", "B3"])

    @pytest.fixture
    def vatican(self):
        """Return a buffer around the Vatican."""
        return ee.Geometry.Point([12.4534, 41.9029]).buffer(100)


class TestClipOnCollection:
    """Test the ``clipOnCollection`` method."""

    def test_clip_on_collection(self, image_instance, fc_instance):
        clipped = image_instance.geetools.clipOnCollection(fc_instance)
        assert clipped.first().bandNames().getInfo() == ["B1", "B2", "B3"]
        assert clipped.size().getInfo() == 2
        assert "Id" in clipped.first().propertyNames().getInfo()

    def test_clip_on_collection_without_properties(self, image_instance, fc_instance):
        clipped = image_instance.geetools.clipOnCollection(fc_instance, 0)
        assert clipped.first().bandNames().getInfo() == ["B1", "B2", "B3"]
        assert clipped.size().getInfo() == 2
        assert "Id" not in clipped.first().propertyNames().getInfo()

    def test_deprecated_method(self, image_instance, fc_instance):
        with pytest.deprecated_call():
            clipped = geetools.tools.image.clipToCollection(image_instance, fc_instance)
            assert clipped.first().bandNames().getInfo() == ["B1", "B2", "B3"]
            assert clipped.size().getInfo() == 2
            assert "Id" in clipped.first().propertyNames().getInfo()

    @pytest.fixture
    def image_instance(self):
        """Return an Image instance."""
        src = "COPERNICUS/S2_SR_HARMONIZED/20200101T100319_20200101T100321_T32TQM"
        return ee.Image(src).select(["B1", "B2", "B3"])

    @pytest.fixture
    def fc_instance(self):
        """Return 2 little buffers in vaticanc city as a featurecollection."""
        return ee.FeatureCollection(
            [
                ee.Feature(ee.Geometry.Point([12.4534, 41.9029]).buffer(50), {"Id": 1}),
                ee.Feature(
                    ee.Geometry.Point([12.4534, 41.9029]).buffer(100), {"Id": 2}
                ),
            ]
        )


class TestBufferMask:
    """Test the ``bufferMask`` method."""

    @pytest.mark.xfail
    def test_buffer_mask(self, image_instance, vatican):
        """I don't know what to test here."""
        assert False


class TestFull:
    """Test the ``full`` method."""

    def test_full(self, vatican):
        image = ee.Image.geetools.full()
        values = image.reduceRegion(ee.Reducer.first(), vatican, 1)
        assert values.getInfo() == {"constant": 0}

    def test_full_with_value(self, vatican):
        image = ee.Image.geetools.full([1])
        values = image.reduceRegion(ee.Reducer.first(), vatican, 1)
        assert values.getInfo() == {"constant": 1}

    def test_full_with_name(self, vatican):
        image = ee.Image.geetools.full([1], ["toto"])
        values = image.reduceRegion(ee.Reducer.first(), vatican, 1)
        assert values.getInfo() == {"toto": 1}

    def test_full_with_lists(self, vatican):
        image = ee.Image.geetools.full([1, 2, 3], ["toto", "titi", "tata"])
        values = image.reduceRegion(ee.Reducer.first(), vatican, 1)
        assert values.getInfo() == {"toto": 1, "titi": 2, "tata": 3}

    def test_deprecated_method(self, vatican):
        with pytest.deprecated_call():
            image = geetools.tools.image.empty()
            values = image.reduceRegion(ee.Reducer.first(), vatican, 1)
            assert values.getInfo() == {"constant": 0}

    @pytest.fixture
    def vatican(self):
        """A 1 m buffer around the Vatican."""
        return ee.Geometry.Point([12.4534, 41.9033]).buffer(100)
