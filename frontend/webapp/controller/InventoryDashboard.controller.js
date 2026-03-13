sap.ui.define(
  [
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/m/MessageBox",
    "sap/ui/model/Filter",
    "sap/ui/model/FilterOperator",
  ],
  function (Controller, JSONModel, MessageBox, Filter, FilterOperator) {
    "use strict";

    var API_BASE = "http://localhost:8000";

    return Controller.extend("myApp.controller.InventoryDashboard", {
      onInit: function () {
        var oModel = new JSONModel({
          summary: {
            total_products: 0,
            low_stock: 0,
            out_of_stock: 0,
            total_stock_value: 0,
          },
          products: [],
        });
        this.getView().setModel(oModel, "inventoryModel");
        this._loadData();
      },

      _loadData: function () {
        var oModel = this.getView().getModel("inventoryModel");
        var sToken = sessionStorage.getItem("token");

        fetch(API_BASE + "/dashboard/inventory", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: sToken ? "Bearer " + sToken : "",
          },
        })
          .then(function (res) {
            if (!res.ok) throw new Error("Failed to load inventory data");
            return res.json();
          })
          .then(function (data) {
            oModel.setProperty("/summary", data.summary || {});
            oModel.setProperty("/products", data.products || []);
          })
          .catch(function (err) {
            console.error(err);
            MessageBox.error("Could not load inventory data.");
          });
      },

      onSearchProducts: function (oEvent) {
        var sQuery = (oEvent.getParameter("newValue") || "").trim();
        var oTable = this.byId("productsTable");
        var oBinding = oTable.getBinding("items");
        if (!oBinding) return;

        if (!sQuery) {
          oBinding.filter([]);
          return;
        }

        oBinding.filter([
          new Filter({
            filters: [
              new Filter("product_name", FilterOperator.Contains, sQuery),
              new Filter("category_name", FilterOperator.Contains, sQuery),
            ],
            and: false,
          }),
        ]);
      },
    });
  },
);
