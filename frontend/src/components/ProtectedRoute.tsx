import React from "react";
import { Navigate } from "react-router-dom";

export const ProtectedRoute: React.FC<{ children: React.ReactElement }> = ({ children }) => {

    // Mock authentication status
    const isAuthenticated: boolean = localStorage.getItem('Authorization') === "true" ? true : false;

    return isAuthenticated ? (
        children
    ) : (
        <Navigate to="/login" replace />
    );
};