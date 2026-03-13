sap.ui.define(
  [
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/m/MessageBox",
  ],
  function (Controller, JSONModel, MessageBox) {
    "use strict";

    var API_BASE = "http://localhost:8000";

    return Controller.extend("myApp.controller.SalesDashboard", {
      onInit: function () {
        var oSalesModel = new JSONModel({
          summary: {
            total_revenue: 0,
            total_orders: 0,
            avg_order_value: 0,
            pending_orders: 0,
          },
          top_products: [],
          monthly: [],
        });
        this.getView().setModel(oSalesModel, "salesModel");
        this._loadData();
      },

      _loadData: function () {
        var oSalesModel = this.getView().getModel("salesModel");
        var sToken = sessionStorage.getItem("token");

        fetch(API_BASE + "/dashboard/sales", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: sToken ? "Bearer " + sToken : "",
          },
        })
          .then(function (res) {
            if (!res.ok) throw new Error("Failed to load sales data");
            return res.json();
          })
          .then(function (data) {
            oSalesModel.setProperty("/summary", data.summary || {});
            oSalesModel.setProperty("/top_products", data.top_products || []);
            oSalesModel.setProperty("/monthly", data.monthly || []);
          })
          .catch(function (err) {
            console.error(err);
            MessageBox.error("Could not load sales data.");
          });
      },
    });
  },
);
