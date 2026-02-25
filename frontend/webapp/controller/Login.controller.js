sap.ui.define(
  ["sap/ui/core/mvc/Controller", "sap/m/MessageToast", "sap/m/MessageBox"],
  function (Controller, MessageToast, MessageBox) {
    "use strict";

    return Controller.extend("myApp.controller.Login", {
      // 🔥 PUT IT HERE
      onInit: function () {
        var oModel = new sap.ui.model.json.JSONModel({
          username: "",
          password: "",
        });
        this.getView().setModel(oModel);
      },

      login: function () {
        var oView = this.getView();
        var oModel = oView.getModel();

        var username = oModel.getProperty("/username");
        var password = oModel.getProperty("/password");

        if (!username || !password) {
          MessageBox.warning("Please enter username and password.");
          return;
        }

        fetch("http://localhost:8000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: username,
            password: password,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Invalid credentials");
            }
            return response.json();
          })
          .then((data) => {
            sap.ui
              .getCore()
              .setModel(
                new sap.ui.model.json.JSONModel({ role: data.role }),
                "userModel",
              );

            sessionStorage.setItem("token", data.access_token);
            sessionStorage.setItem("role", data.role);

            var oRouter = this.getOwnerComponent().getRouter();

            switch (data.role) {
              case "ceo":
                oRouter.navTo("CEODashboard");
                break;
              case "sales_manager":
                oRouter.navTo("SalesDashboard");
                break;
              case "inventory_manager":
                oRouter.navTo("InventoryDashboard");
                break;
              default:
                MessageBox.error("Unknown role");
            }
          })
          .catch((error) => {
            MessageBox.error("Login failed. Please check your credentials.");
            console.error(error);
          });
      },
    });
  },
);
