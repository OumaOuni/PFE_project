sap.ui.define(
  [
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/m/MessageToast",
    "sap/m/MessageBox",
  ],
  function (Controller, JSONModel, MessageToast, MessageBox) {
    "use strict";

    return Controller.extend("myApp.controller.ADMINDashboard", {
      onInit: function () {
        var oUserModel = new JSONModel();
        this.getView().setModel(oUserModel, "userModel");
      },

      onOpenAddUserDialog: function () {
        this.byId("addUserDialog").open();
      },
      onCancelAddUser: function () {
        this.byId("addUserDialog").close();
      },
      onValidateInputs: function () {
        const username = this.byId("usernameInput").getValue().trim();
        const email = this.byId("emailInput").getValue().trim();
        const password = this.byId("passwordInput").getValue().trim();
        const role = this.byId("roleInput").getSelectedKey().trim();
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        let isValid = true;

        if (email.length > 0 && !emailRegex.test(email)) {
          this.byId("emailInput").setValueState("Error");
          this.byId("emailInput").setValueStateText(
            "Enter a valid email address",
          );
          isValid = false;
        } else {
          this.byId("emailInput").setValueState("None");
          this.byId("emailInput").setValueStateText("");
        }

        isValid =
          isValid &&
          username.length > 0 &&
          email.length > 0 &&
          password.length > 0 &&
          role.length > 0;

        this.byId("addUserBtn").setEnabled(isValid);
      },
      onAddUser: async function () {
        const username = this.byId("usernameInput").getValue();
        const email = this.byId("emailInput").getValue();
        const password = this.byId("passwordInput").getValue();
        const role = this.byId("roleInput").getSelectedKey();

        try {
          const response = await fetch("http://127.0.0.1:8000/users", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password, role }),
          });

          if (response.ok) {
            sap.m.MessageToast.show("User added successfully");
            this.byId("addUserDialog").close();
          } else {
            const errorData = await response.json();
            sap.m.MessageToast.show(errorData.detail || "Failed to add user");
            this.byId("emailInput").setValueState("Error");
            this.byId("emailInput").setValueStateText(errorData.detail);
          }
        } catch (error) {
          // Network or other unexpected errors
          sap.m.MessageToast.show("Network error: " + error.message);
          console.error(error);
        }
      },
      onEditUser: async function (oEvent) {
        const oItem = oEvent.getSource().getParent().getParent();
        const oContext = oItem.getBindingContext("userModel");
        const user = oContext.getObject();

        // Simple prompt for demo (replace with Dialog)
        const username = prompt("Username:", user.username);
        const email = prompt("Email:", user.email);
        const password = prompt("Password: (leave blank to keep unchanged)");
        const role = prompt("Role:", user.role);

        if (!username || !email || !role) return; // password can be empty
        // keep existing values if user leaves prompt blank
        const usernameFinal = username || user.username;
        const emailFinal = email || user.email;
        const roleFinal = role || user.role;

        // Prepare payload
        const payload = {
          username: usernameFinal,
          email: emailFinal,
          role: roleFinal,
        };
        if (password && password.trim() !== "") {
          payload.password = password;
        }

        try {
          const response = await fetch(
            `http://127.0.0.1:8000/users/${user.id}`,
            {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload),
            },
          );

          if (response.ok) {
            const updatedUser = await response.json();
            const oUserModel = this.getView().getModel("userModel");
            oUserModel.setProperty(oContext.getPath(), updatedUser); // update all fields at once
            alert("User updated!");
          }
        } catch (err) {
          console.error("Failed to edit user:", err);
        }
      },
      onDeleteUser: async function (oEvent) {
        const oItem = oEvent.getSource().getParent().getParent();
        const oContext = oItem.getBindingContext("userModel");
        const user = oContext.getObject();

        if (!confirm(`Delete user ${user.username}?`)) return;

        try {
          const response = await fetch(
            `http://127.0.0.1:8000/users/${user.id}`,
            {
              method: "DELETE",
            },
          );

          if (response.ok) {
            const oUserModel = this.getView().getModel("userModel");
            const users = oUserModel.getProperty("/users");
            const index = users.findIndex((u) => u.id === user.id);
            users.splice(index, 1);
            oUserModel.setProperty("/users", users);
            alert("User deleted!");
          }
        } catch (err) {
          console.error("Failed to delete user:", err);
        }
      },
    });
  },
);
