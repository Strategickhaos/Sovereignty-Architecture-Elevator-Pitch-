import React from "react";
import { createRoot } from "react-dom/client";
import SAGCOFirewall from "./SAGCOFirewall.jsx";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <SAGCOFirewall />
  </React.StrictMode>
);
