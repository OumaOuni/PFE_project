sap.ui.define(
  [
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/ui/model/odata/v2/ODataModel",
  ],
  function (Controller, JSONModel, ODataModel) {
    "use strict";

    return Controller.extend("myApp.controller.CEODashboard", {
      onInit: async function () {
        var oKpiModel = new JSONModel();
        this.getView().setModel(oKpiModel, "kpiModel");

        try {
          // Fetch KPIs
          const kpiResponse = await fetch("http://127.0.0.1:8000/kpis");
          const kpiData = await kpiResponse.json();

          // Fetch Sales
          const salesResponse = await fetch("http://127.0.0.1:8000/sales");
          const salesData = await salesResponse.json();

          // Fetch Trend
          const trendResponse = await fetch("http://127.0.0.1:8000/trend");
          const trendData = await trendResponse.json();

          // Fetch Distribution
          const distResponse = await fetch(
            "http://127.0.0.1:8000/distribution",
          );
          const distData = await distResponse.json();

          // Set all data in one JSON model
          oKpiModel.setData({
            kpi: {
              revenue: kpiData.total_revenue,
              users: kpiData.active_users,
              conversion: kpiData.conversion_rate,
              growth: kpiData.growth_rate,
            },
            sales: salesData,
            trend: trendData,
            distribution: distData,
          });

          const userResponse = await fetch("http://127.0.0.1:8000/users");
          const userData = await userResponse.json();
          oUserModel.setData({
            users: userData,
          });
        } catch (err) {
          console.error("Failed to load data from API:", err);
        }
      },
      // =================== CRUD FUNCTIONS ===================
    });
  },
);
