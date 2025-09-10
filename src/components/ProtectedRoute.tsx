import React from "react";
import { Navigate } from "react-router-dom";

interface ProtectedRouteProps {
  children: React.ReactElement;
  allowedRoles?: string[]; // ✅ Allow role-based protection
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  allowedRoles,
}) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  console.log("[ProtectedRoute] Checking access:", {
    token,
    role,
    allowedRoles,
  });

  // If no token, redirect to login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // If allowedRoles is defined and current role is not in it, redirect to login
  if (allowedRoles && !allowedRoles.includes(role || "")) {
    console.warn("[ProtectedRoute] Role not allowed:", role);
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
