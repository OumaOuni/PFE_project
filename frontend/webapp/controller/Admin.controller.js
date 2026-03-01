sap.ui.define(
  [
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/viz/ui5/data/FlattenedDataset",
    "sap/viz/ui5/controls/common/feeds/FeedItem",
  ],
  function (Controller, JSONModel, FlattenedDataset, FeedItem) {
    "use strict";

    return Controller.extend("myApp.controller.Admin", {
      onInit: function () {
        // Sample data
        var oData = {
          sales: [
            { month: "Jan", revenue: 5000 },
            { month: "Feb", revenue: 7000 },
            { month: "Mar", revenue: 6000 },
          ],
        };

        var oModel = new JSONModel(oData);
        this.getView().setModel(oModel);

        var oVizFrame = this.byId("idVizFrame");

        var oDataset = new FlattenedDataset({
          dimensions: [
            {
              name: "Month",
              value: "{month}",
            },
          ],
          measures: [
            {
              name: "Revenue",
              value: "{revenue}",
            },
          ],
          data: {
            path: "/sales",
          },
        });

        oVizFrame.setDataset(oDataset);

        oVizFrame.addFeed(
          new FeedItem({
            uid: "valueAxis",
            type: "Measure",
            values: ["Revenue"],
          }),
        );

        oVizFrame.addFeed(
          new FeedItem({
            uid: "categoryAxis",
            type: "Dimension",
            values: ["Month"],
          }),
        );
      },
    });
  },
);
