# coding: utf-8
"""
    assetic.layertools  (layertools.py)
    Tools to assist with using arcgis integration with assetic
"""
from __future__ import absolute_import

import arcpy
import sys
import logging
from assetic.tools.shared import LayerToolsBase

from .esri_messager import EsriMessager

try:
    import pythonaddins
except ImportError:
    # ArcGIS Pro doesn't have this library
    pass
from typing import List, Any
import assetic
import six
from arcgis2geojson import arcgis2geojson
import json


class LayerTools(LayerToolsBase):
    """
    Class to manage processes that relate to a GIS layer

    layerconfig arg is not mandatory and during testing is not passed in.
    """

    def __init__(self, config=None):
        if config is None:
            from assetic_esri import Config
            config = Config()

        super(LayerTools, self).__init__(config)

        self.logger = logging.getLogger(__name__)

        # initialise common tools so can use messaging method
        self.commontools = EsriMessager()
        self.commontools.force_use_arcpy_addmessage = config.force_use_arcpy_addmessage

    @property
    def is_valid_config(self):
        # type: () -> bool
        """
        Asset Layer Configuration
        Cache the XML content so that we don't continually reload it as we
        access it in _get_cat_config
        :return:
        """
        return self.xmlconf._is_valid_config

    @property
    def fl_layerconfig(self):
        # type: () -> dict
        """
        Functional Location Layer configuration
        Cache the XML content so that we don't continually reload it
        :return:
        """
        return self.config.layerconfig.fcnlayerconfig

    def _ind_update_assets(self, cursor, lyr, dialog):
        """
        Invidividually updates each asset using the passed in cursor
        object and layer information.

        :param cursor: database cursor with attached layer information
        :param lyr: <Layer>
        :param dialog: allows interacting with the ArcGIS console
        :return:
        """

        # create and asset pass and fail counters
        iFail = 0
        iPass = 0

        sel_set = lyr.getSelectionSet()
        if sel_set is None:
            self.logger.error(
                "No features selected.")
            return
        else:
            # get number of records to process for use with timing dialog
            if sel_set:
                selcount = len(sel_set)
            else:
                # haven't run query yet so just set a dummy count.
                selcount = 1

        lyr_config, fields, idfield = self.xmlconf.get_layer_config(lyr, lyr.name, "update")

        cnt = 1.0

        for row in cursor:
            chk = self._update_asset(row, lyr_config, fields)

            if self.commontools.is_desktop:
                if self.config.force_use_arcpy_addmessage:
                    # Using the progressor
                    arcpy.SetProgressorLabel(
                        "Updating Assets for layer {0}.\nProcessing "
                        "feature {1} of {2}".format(
                            lyr.name, int(cnt), selcount))
                    arcpy.SetProgressorPosition()
                else:
                    dialog.description = \
                        "Updating Assets for layer {0}." \
                        "\nProcessing feature {1} of {2}".format(
                            lyr.name, int(cnt), selcount)
                    dialog.progress = cnt / selcount * 100
            else:
                msg = "Updating Assets for layer {0}." \
                      "\nProcessing feature {1} of {2}".format(
                    lyr.name, int(cnt), selcount)
                self.commontools.new_message(msg)
                self.logger.info(msg)
            if not chk:
                iFail = iFail + 1
            else:
                iPass = iPass + 1

            # increment counter
            cnt = cnt + 1

        return iFail, iPass

    def create_assets(self, lyr, query=None):
        return self.create_asset(lyr, query)

    def create_asset(self, lyr, query=None):
        # type: (arcpy._mp.Layer, str) -> None
        """
        For the given layer create new assets for the selected features only if
        features have no assetic guid.

        :param lyr: is the layer to process (not layer name but ArcMap layer)
        :param query: optionally apply query filter
        """
        if not self._is_valid_config:
            self.logger.error("Invalid or missing configuration file, "
                              "asset creation aborted.")
            return
        self.logger.debug("create_asset. Layer={0}".format(lyr.name))

        # get configuration for layer
        lyr_config, fields, idfield = self.xmlconf.get_layer_config(lyr, lyr.name, "create")

        if lyr_config is None:
            self.logger.error("Returning early as layerfile "
                              "has been misconfigured. See log output.")
            return

        # get number of records to process for use with timing dialog
        sel_set = lyr.getSelectionSet()
        if sel_set is None and query is None:
            self.logger.debug(
                "No features selected - must pass in valid 'where clause'.")
            return
        else:
            # get number of records to process for use with timing dialog
            if sel_set:
                selcount = len(sel_set)
            else:
                # haven't run query yet so just set a dummy count.
                selcount = 1

        progress_tool = self.commontools.get_progress_dialog(
            self.config.force_use_arcpy_addmessage, lyr.name, selcount)

        if self.commontools.is_desktop is False:
            selcount = 0

        prog_cnter = {
            "pass_cnt": 0,
            "fail_cnt": 0,
            "skip_cnt": 0,
            "partial_cnt": 0,
        }

        with progress_tool as dialogtools:
            if self.commontools.is_desktop and \
                    not self.config.force_use_arcpy_addmessage:
                dialog = dialogtools
                dialog.title = "Assetic Integration"
                dialog.description = "Creating Assets for layer {0}.".format(
                    lyr.name)
                dialog.canCancel = False

            # create an update cursor to allow updating
            with arcpy.da.UpdateCursor(lyr, fields, query) as cursor:

                # iterator to count number rows processed
                cnt = 1.0
                for row in cursor:
                    if self.commontools.is_desktop:
                        if self.config.force_use_arcpy_addmessage:
                            # Using the progressor
                            arcpy.SetProgressorLabel(
                                "Creating Assets for layer {0}.\nProcessing "
                                "feature {1} of {2}".format(
                                    lyr.name, int(cnt), selcount))
                            arcpy.SetProgressorPosition()
                        else:
                            dialog.description = \
                                "Creating Assets for layer {0}." \
                                "\nProcessing feature {1} of {2}".format(
                                    lyr.name, int(cnt), selcount)
                            dialog.progress = cnt / selcount * 100

                    drow = dict(zip(fields, row))

                    # attempt to create asset, components, dimensions
                    result_code = self._new_asset(drow, lyr_config, fields)

                    if result_code in \
                            [self.results['success'], self.results['partial']]:
                        # convert to a list in order of fields
                        lrow = [drow[f] for f in fields]

                        if result_code == self.results['success']:
                            suc = "successful"
                            prog_cnter['pass_cnt'] += 1
                        else:
                            suc = "partially successful"
                            prog_cnter['partial_cnt'] += 1
                        self.logger.debug(
                            "Update of asset ID {0}, updating ArcGIS row."
                            "".format(suc))

                        cursor.updateRow(lrow)

                    elif result_code == self.results['skip']:
                        prog_cnter['skip_cnt'] += 1
                    else:
                        prog_cnter['fail_cnt'] += 1

                    cnt = cnt + 1

        msg = ("Finished {0} Asset Creation: {1} Assets created ({2} partially"
               " created), {3} skipped (already created)"
               .format(lyr.name, str(prog_cnter['pass_cnt'])
                       , str(prog_cnter['partial_cnt'])
                       , str(prog_cnter['skip_cnt'])
                       ))

        if prog_cnter['fail_cnt'] > 0:
            msg = msg + ", {0} failed. See log for further details ({1})." \
                        "".format(
                str(prog_cnter['fail_cnt']), self.logfilename)

        self.commontools.new_message(msg)

    @staticmethod
    def get_rows(lyr, fields, query=None):
        """
        A method to retrieve rows from a cursor and return them in
        dict form, if arcpy is imported.

        If not, expects lyr object to be iterable and return dicts
        of {col: val}.

        :param lyr:
        :param fields:
        :param query:
        :return:
        """
        rows = []

        if 'arcpy' in sys.modules:
            with arcpy.da.SearchCursor(lyr, fields, query) as cursor:

                # extract all of the important information out of the
                # cursor object
                for row in cursor:
                    # create a dict object from the cursor fields and
                    # the row values

                    dict_row = dict(zip(fields, row))

                    rows.append(dict_row)
        else:
            for row in lyr:
                rows.append(row)

        return rows

    def bulk_update_rows(self, rows, lyr, lyr_config):
        """
        Initiate bulk update of assets and components etc via Data Exchange
        :param rows: list of dictionaries, each row is a record from GIS
        :param lyr: the GIS layer being processed
        :param lyr_config: The configuration settings for the layer from
        the XML file
        :return: valid rows - the rows for where the asset actually exists
        """
        if len(lyr_config["all_calc_output_fields"]) > 0:
            # there are calculated fields to manage
            for row in rows:
                for calculation in lyr_config["calculations"]:
                    calc_val = self._calc_tools.run_calc(
                        calculation["calculation_tool"],
                        calculation["input_fields"]
                        , row, lyr_config["layer"])
                    if calc_val:
                        row[calculation["output_field"]] = calc_val

        lyr_name = lyr.name
        message = 'Commencing Data Exchange bulk update initiation'
        self.commontools.new_message(message, "Assetic Integration")

        # Bulk update assets will return valid rows, invalid rows are asset id
        # not found or disposed assets
        chk, valid_rows = self.gis_tools.bulk_update_assets(rows, lyr_name)
        if chk != 0:
            message = "Error encountered bulk updating assets"
            self.commontools.new_message(message, "Assetic Integration")
        if len(valid_rows) == 0:
            self.commontools.new_message("No valid assets for update"
                                         , "Assetic Integration")
        self.gis_tools.bulk_update_components(valid_rows, lyr_name)
        self.gis_tools.bulk_update_addresses(valid_rows, lyr_name)
        self.gis_tools.bulk_update_networkmeasures(valid_rows, lyr_name)
        self.gis_tools.bulk_update_asset_fl_assoc(valid_rows, lyr_name)
        if lyr_config["upload_feature"]:
            self.bulk_update_spatial(valid_rows, lyr, lyr_config)

        message = 'Completed initiating Data Exchange updates, updates may ' \
                  'still be in progress. Check Data Exchange History page'
        self.commontools.new_message(message, "Assetic Integration")
        return chk, valid_rows

    def individually_update_rows(self, rows, lyr_config, fields, dialog):
        # type: (List[dict], dict, List[str], Any) -> None
        """
        Iterates over the rows of the layerfile and updates each asset
        using API calls.

        :param rows: <List[dict]> a list of dicts where keys are the
        column names and values are cell contents
        :param lyr_config: <dict> dict defining the relationship
        between xml nodes and the layer's column values
        :param fields: <List[str]> a list of column names from the layer
        :param dialog: <Unsure> arcpy dialog object that allows arcpy
        messages to be pushed to console
        :return:
        """

        lyrname = lyr_config['layer']

        total = len(rows)

        # initialise counters for the log messages
        num_pass = 0
        num_fail = 0

        for i, row in enumerate(rows):
            success = self._update_asset(row, lyr_config, fields)

            if self.commontools.is_desktop:
                if self.config.force_use_arcpy_addmessage:
                    # Using the progressor
                    arcpy.SetProgressorLabel(
                        "Updating Assets for layer {0}.\nProcessing "
                        "feature {1} of {2}".format(
                            lyrname, i + 1, total))
                    arcpy.SetProgressorPosition()
                else:
                    dialog.description = \
                        "Updating Assets for layer {0}." \
                        "\nProcessing feature {1} of {2}".format(
                            lyrname, i + 1, total)
                    dialog.progress = (i + 1 / total) * 100
            else:
                msg = "Updating Assets for layer {0}." \
                      "\nProcessing feature {1} of {2}".format(
                    lyrname, i + 1, total)
                self.commontools.new_message(msg)
                self.logger.info(msg)

            if success:
                num_pass = num_pass + 1
            else:
                num_fail = num_fail + 1

        message = "Finished {0} Asset Update, {1} assets updated".format(
            lyrname, str(num_pass))

        if num_fail > 0:
            message = "{0}, {1} assets not updated. (Check log file '{2}')" \
                      "".format(message, str(num_fail), self.logfilename)

        self.commontools.new_message(message, "Assetic Integration")

    def update_assets(self, lyr, query=None):
        """
        For the given layer update assets for the selected features only
        where features have an assetic guid/asset id.
        :param lyr: is the layer to process (not layer name but ArcMap layer)
        :param query: optional attribute query to get selection
        """
        if not self._is_valid_config:
            self.logger.error("Invalid or missing configuration file, "
                              "asset update aborted.")
            return
        # get layer configuration from xml file
        lyr_config, fields, idfield = self.xmlconf.get_layer_config(lyr, lyr.name, "update")

        if lyr_config is None:
            return

        # "returns the layer's selection as a python set of object IDs"
        sel_set = lyr.getSelectionSet()
        if sel_set is None and query is None:
            self.logger.debug("No features selected - must pass in valid"
                              " 'where clause'.")
            return
        else:
            # get number of records to process for use with timing dialog
            if sel_set:
                selcount = len(sel_set)
            else:
                # haven't run query yet so just set a dummy count.
                selcount = 1

        progress_tool = self.commontools.get_progress_dialog(
            self.config.force_use_arcpy_addmessage, lyr.name, selcount)

        with progress_tool as dialog:
            if self.commontools.is_desktop and \
                    not self.config.force_use_arcpy_addmessage:
                dialog.title = "Assetic Integration"
                dialog.description = "Updating assets for layer {0}".format(
                    lyr.name)
                dialog.canCancel = False

            # retrieve rows from layer
            rows = self.get_rows(lyr, fields, query)

            if len(rows) > self._bulk_threshold:
                chk, valid_rows = self.bulk_update_rows(rows, lyr, lyr_config)
            else:
                self.individually_update_rows(rows, lyr_config, fields, dialog)

    def display_in_assetic(self, lyr):
        """
        Open Assetic and display the first selected feature in layer
        Use config to determine if Asset or FL
        :param lyr: The layer find selected features.  Not layer name,
        layer object
        """

        # is it an asset layer?
        for j in self._assetconfig:
            if j["layer"] == lyr.name:
                self.display_asset(lyr)
        else:
            lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(
                lyr, lyr.name, "display")
            if lyr_config:
                self.display_fl(lyr, lyr_config, idfield)

    def display_asset(self, lyr, lyr_config=None, idfield=None):
        """
        Open assetic and display the first selected feature in layer
        :param lyr_config: config for layer as read from XML
        :param idfield: the assetic ID field
        :return:
        :param lyr: The layer find selected assets.  Not layer name,layer object
        """
        # get layer config details
        if not lyr_config:
            lyr_config, fields, idfield = self.xmlconf.get_layer_config(lyr, lyr.name, "display")
        if not lyr_config:
            return

        self.logger.debug("Layer: {0}, id field: {1}".format(
            lyr.name, idfield))
        try:
            features = arcpy.da.SearchCursor(lyr, idfield)
            row = features.next()
            assetid = str(row[0])
        except Exception as ex:
            msg = "Unexpected Error Encountered, check log file '{0}'".format(
                self.logfilename)
            self.commontools.new_message(msg)
            self.logger.error(str(ex))
            return
        if assetid is None or assetid.strip() == "":
            msg = "Asset ID or Asset GUID is NULL.\nUnable to display asset"
            self.commontools.new_message(msg)
            self.logger.warning(str(msg))
            return
        self.logger.debug("Selected Asset to display: [{0}]".format(
            assetid))
        # Now launch Assetic
        apihelper = assetic.APIHelper(self.asseticsdk.client)
        apihelper.launch_assetic_asset(assetid)

    def display_fl(self, lyr, lyr_config=None, idfield=None):
        """
        Open assetic and display the first selected feature in layer
        :param lyr: The layer find selected assets. Not layer name,layer object
        :param lyr_config: config for layer as read from XML
        :param idfield: the assetic ID field
        :return:
        """
        # get layer config details
        if not lyr_config:
            lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(
                lyr, lyr.name, "display")
        if not lyr_config:
            return

        self.logger.debug("Layer: {0}, id field: {1}".format(
            lyr.name, idfield))
        try:
            features = arcpy.da.SearchCursor(lyr, idfield)
            row = features.next()
            flid = str(row[0])
        except Exception as ex:
            msg = "Unexpected Error Encountered, check log file '{0}'".format(
                self.logfilename)
            self.commontools.new_message(msg)
            self.logger.error(str(ex))
            return
        if flid is None or flid.strip() == "":
            msg = "Functional Location ID or GUID is NULL.\nUnable to " \
                  "display Functional Location"
            self.commontools.new_message(msg)
            self.logger.warning(str(msg))
            return
        self.logger.debug(
            "Selected Functional Location to display: [{0}]".format(flid))
        # Now launch Assetic
        apihelper = assetic.APIHelper(self.asseticsdk.client)
        apihelper.launch_assetic_functional_location(flid)

    def get_geom_wkt(self, outsrid, geometry):
        """
        Get the well known text for a geometry in 4326 projection
        :param outsrid: The projection EPSG code to export WKT as (integer)
        :param geometry: The input geometry
        :returns: wkt string of geometry in the specified projection
        """
        tosr = arcpy.SpatialReference(outsrid)
        new_geom = geometry.projectAs(tosr)
        wkt = new_geom.WKT
        return wkt

    def get_geom_geojson(self, outsrid, geometry, centroid=None):
        """
        Get the geojson for a geometry in 4326 projection
        :param outsrid: The projection EPSG code to export WKT as (integer)
        :param geometry: The input geometry
        :param centroid: The geometry centroid, use for polygons in case polygon
        orientation is wrong.  Optional
        :returns: wkt string of geometry in the specified projection
        """
        tosr = arcpy.SpatialReference(outsrid)

        if "curve" in geometry.JSON:
            # arcs and circles not supported by geoJson
            # the WKT doesn't define arcs so use it
            simple_geom = arcpy.FromWKT(geometry.WKT,
                                        geometry.spatialReference)
            new_geom = simple_geom.projectAs(tosr)
        else:
            new_geom = geometry.projectAs(tosr)
        # now convert to geojson
        geojsonstr = arcgis2geojson(new_geom.JSON)
        geojson = json.loads(geojsonstr)
        centroid_geojson = None
        if "type" in geojson and geojson["type"].lower() == "polygon":
            if isinstance(centroid, tuple) and len(centroid) == 2:
                point = arcpy.Point(centroid[0], centroid[1])
                pt_geometry = arcpy.PointGeometry(point
                                                  , geometry.spatialReference)
                new_centroid = pt_geometry.projectAs(tosr)
                centroid_geojson_str = arcgis2geojson(new_centroid.JSON)
                centroid_geojson = json.loads(centroid_geojson_str)
        if "GeometryCollection" not in geojson:
            # Geojson is expected to include collection, but arcgis2geojson
            # does not include it
            if centroid_geojson:
                fullgeojson = {
                    "geometries": [geojson, centroid_geojson]
                    , "type": "GeometryCollection"}
            else:
                fullgeojson = {
                    "geometries": [geojson]
                    , "type": "GeometryCollection"}
        else:
            # not try to include centroid, too messy.  Am not expecting to hit
            # this case unless arcgis2geojson changes
            fullgeojson = geojson

        return fullgeojson

    def GetEventAssetID(self, geometryObj, oidList, layerList):
        """
        Gets the guid for an asset feature that has been deleted or moved
        https://github.com/savagemat/PythonEditCounter/blob/master/Install/PythonEditCounter_addin.py
        :param geometryObj: The feature that was deleted or moved
        :param oidList: A list of OIDs as integers
        :param layerList: Layers in the workspace
        :returns: Unique Assetic ID of the feature that was deleted/moved
        """
        for lyr in layerList:
            if lyr.isFeatureLayer:
                ##get layer config details
                lyr_config, fields, idfield = self.xmlconf.get_layer_config(
                    lyr, lyr.name, "delete")
                if idfield != None:
                    oidField = arcpy.Describe(lyr).OIDFieldName
                    query = "{0} in {1}".format(oidField, str(oidList).replace(
                        '[', '(').replace(']', ')'))
                    with arcpy.da.SearchCursor(lyr,
                                               [oidField, "SHAPE@", idfield],
                                               where_clause=query) as rows:
                        for row in rows:
                            geom = row[1]
                            if geom.JSON == geometryObj.JSON:
                                ##return the assetid and the layer it belongs to
                                return row[2], lyr

        # feature is not a valid asset so return nothing
        return None, None

    def undo_edit(self, lyr):
        """
        Not implemented.  Works outside of edit session but not in
        need to figure out how to access
        """
        desc = arcpy.Describe(lyr)
        workspace = desc.path
        with arcpy.da.Editor(workspace) as edit:
            edit.abortOperation()

    def get_layer_asset_guid(self, assetid, lyr_config):
        """
        **Has been moved to XMLConf**

        Get the asset guid for an asset.  Used where "id" is not in the
        configuration.  If it is then it is assumed the assetid is a guid
        :param assetid: The assetid - may be guid or friendly
        :param lyr_config: the layer
        :returns: guid or none
        """
        return self.xmlconf.get_layer_asset_guid(assetid, lyr_config)

    def decommission_asset(self, assetid, lyr_config, comment=None):
        """
        Set the status of an asset to decommisioned
        :param assetid: The asset GUID (TODO support friendly ID)
        :param lyr_config: config details for layer
        :param comment: A comment to accompany the decommision
        :returns: 0=no error, >0 = error
        """

        return 1

    @staticmethod
    def get_fl_layer_fields_dict(lyr_config):

        cores = lyr_config['fl_corefields']
        coredefs = lyr_config['fl_coredefaults']

        layer_dict = {
            'id': cores['id'],
            'functional_location_id': cores['functional_location_id'],
            'functional_location_name': cores['functional_location_name'],
            'functional_location_type': coredefs['functional_location_type'],
        }

        return layer_dict

    def create_funclocs_from_layer(self, lyr, query=None):
        # type: (Any, str) -> (int, int)
        """
        Iterates over the rows in a passed in layer (narrowed down by
        optional query) and creates functional locations defined in
        the data.

        Returns the number of successful and failed functional
        locations.

        :param lyr: passed in arcgis layerfile
        :param query: query to select certain attributes
        :return: number created, number failed
        """
        if not self._is_valid_config:
            self.logger.error("Invalid or missing configuration file, "
                              "functional location creation aborted.")
            return

        lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(lyr, lyr.name, "create")
        if (lyr_config is None) and (fields is None):
            self.commontools.new_message(
                "Unable to process functional location layer '{0}' due to "
                "missing configuration".format(lyr.name))
            # return indication that nothing was processed
            return 0, 0

        has_lyr_fl_type = 'functional_location_type' in fields

        fl_corefields = lyr_config['fl_corefields']
        fl_coredefaults = lyr_config['fl_coredefaults']

        attrs = lyr_config['fl_attributefields']
        def_attrs = lyr_config['fl_attributedefaults']

        success = 0
        fail = 0
        with arcpy.da.UpdateCursor(lyr, fields, query) as cursor:
            for row in cursor:

                if has_lyr_fl_type:
                    # many fltypes in a single layer
                    fltype = row[fl_corefields['functional_location_type']]
                else:
                    # single fltype per layer
                    fltype = fl_coredefaults['functional_location_type']

                drow = dict(zip(fields, row))

                flid = drow[fl_corefields['functional_location_id']]

                if flid in ['', None]:
                    # no FL ID defined. attempt to retrieve by name and type
                    flrepr = self.fltools.get_functional_location_by_name_and_type(
                        drow[fl_corefields['functional_location_name']]
                        , fltype)
                else:
                    # FL ID defined. attempt to retrieve by ID
                    # if FL doesn't exist we assume that autoid generation
                    # is off which is why the ID is already set in the layer
                    flrepr = self.fltools.get_functional_location_by_id(flid)

                if flrepr is not None:
                    # FL already exists!
                    self.commontools.new_message(
                        "Functional Location {0} already exists".format(
                            flrepr.functional_location_name
                        ))
                    fail += 1
                    continue

                # Doesn't appear to be an existing FL so create.
                flrepr = self._create_fl_from_row(
                    drow, fl_corefields, fltype, attrs, def_attrs)
                if flrepr is None:
                    # Error creating FL
                    fail += 1
                    continue

                # update row with new information - ID, GUID, etc.
                updfields = [fl_corefields[f] for f in [
                    'functional_location_id', 'id'] if f in fl_corefields]
                rev = {v: k for k, v in six.iteritems(fl_corefields)}
                for f in updfields:
                    row[fields.index(f)] = (flrepr.__getattribute__(rev[f]))

                cursor.updateRow(row)
                success += 1

        message = "Finished {0} Functional Location Creation, {1} Functional" \
                  " Locations created".format(lyr.name, str(success))

        if fail > 0:
            message = "{0}, {1} Functional Locations not created. (Check " \
                      "logfile {2})".format(
                message, str(fail), self.logfilename)

        self.commontools.new_message(message, "Assetic Integration")

        return success, fail

    def update_funclocs_from_layer(self, lyr, query=None):
        # type: (Any, str) -> (int, int)
        """
        Iterates over the rows in a passed in layer (narrowed down by
        optional query) and updates functional locations defined in
        the data.

        Returns the number of successful and failed updates of functional
        locations.

        :param lyr: passed in arcgis layerfile
        :param query: query to select certain attributes
        :return: number created, number failed
        """
        if not self._is_valid_config:
            self.logger.error("Invalid or missing configuration file, "
                              "Functional Location update aborted.")
            return

        lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(lyr, lyr.name, "update")
        if lyr_config is None and fields is None:
            msg = "Unable to process functional location layer '{0}' due to " \
                  "missing configuration".format(lyr.name)
            self.commontools.new_message(msg)
            self.logger.error(msg)
            # return indication that nothing was processed
            return 0, 0

        fl_corefields = lyr_config['fl_corefields']
        fl_coredefaults = lyr_config['fl_coredefaults']

        has_lyr_fl_type = False
        if 'functional_location_type' in fl_corefields:
            has_lyr_fl_type = True
        elif 'functional_location_type' not in fl_coredefaults:
            # need to have functional location type
            msg = "Unable to process functional location layer '{0}' due to " \
                  "missing functional location type".format(lyr.name)
            self.commontools.new_message(msg)
            self.logger.error(msg)
            # return indication that nothing was processed
            return 0, 0

        attrs = lyr_config['fl_attributefields']
        def_attrs = lyr_config['fl_attributedefaults']
        all_attr_fields = attrs.keys() + def_attrs.keys()

        success = 0
        fail = 0
        with arcpy.da.SearchCursor(lyr, fields, query) as cursor:
            for row in cursor:

                if has_lyr_fl_type:
                    # many fltypes in a single layer
                    fltype = row[fl_corefields['functional_location_type']]
                else:
                    # single fltype per layer defined in defaults
                    fltype = fl_coredefaults['functional_location_type']

                drow = dict(zip(fields, row))

                flid = drow[fl_corefields['functional_location_id']]

                fl_guid = None
                if "id" in fl_corefields and fl_corefields['id'] in drow:
                    fl_guid = drow[fl_corefields['id']]

                if flid in ['', None] and fl_guid in ['', None]:
                    # no FL ID defined. attempt to retrieve by name and type
                    flrepr = self.fltools.get_functional_location_by_name_and_type(
                        drow[fl_corefields['functional_location_name']]
                        , fltype, all_attr_fields)
                else:
                    # FL ID defined. attempt to retrieve by ID
                    if fl_guid:
                        flrepr = self.fltools.get_functional_location_by_id(
                            fl_guid, all_attr_fields)
                    else:
                        flrepr = self.fltools.get_functional_location_by_id(
                            flid, all_attr_fields)
                if flrepr is None:
                    # No FL found so move to next record
                    self.commontools.new_message(
                        "Unable to retrieve Functional Location {0} for "
                        "update".format(
                            drow[fl_corefields['functional_location_name']]
                        ))
                    fail += 1
                    continue

                # FL exists, check if the attributes are different
                # and then post if they are
                row_attrs = self._retrieve_fl_attrs_from_row(drow, attrs,
                                                             def_attrs)

                if row_attrs != flrepr.attributes or \
                        flrepr.functional_location_name != drow[
                    fl_corefields['functional_location_name']]:
                    # e.g. something has changed so update attributes with GIS
                    # attributes, and name in case it changed (not allow
                    # change to FL type or id)
                    flrepr.attributes = row_attrs
                    flrepr.functional_location_name = drow[
                        fl_corefields['functional_location_name']]
                    flepr = self.fltools.update_functional_location(flrepr)
                    if flepr:
                        success += 1
                    else:
                        fail += 1
                else:
                    # indicate success, just don't attempt update
                    success += 1

        message = "Finished {0} Functional Location Update, {1} Functional " \
                  "Locations updated".format(lyr.name, str(success))

        if fail > 0:
            message = "{0}, {1} Functional Locations not updated. (Check " \
                      "logfile {2})".format(
                message, str(fail), self.logfilename)

        self.commontools.new_message(message, "Assetic Integration")

        return success, fail
