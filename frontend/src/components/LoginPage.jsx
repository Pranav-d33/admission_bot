import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("super-admin"); // Default role
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      // Simulate an API call
      const response = await fakeLoginAPI(email, password, role);

      if (response.success) {
        login(response.data); // Save user data in context
        navigate(`/${response.data.role}`);
      } else {
        alert("Invalid credentials!");
      }
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-200">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="border p-2 rounded mb-4"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="border p-2 rounded mb-4"
      />
      <p>&darr; Choose role &darr;</p>
      <select
        value={role}
        onChange={(e) => setRole(e.target.value)}
        className="border p-2 rounded mb-4 border-2 border-gray-600"
      >
        <option value="super-admin">Super Admin</option>
        <option value="gov-verifier">Government Verifier</option>
        <option value="institution-admin">Institution Admin</option>
        <option value="institution-provider">Institution Provider</option>
      </select>
      <button
        onClick={handleLogin}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Login
      </button>

      <div>
        <p>Test credentials</p>
        <ul>
            <li> email: "provider@test.com", password: "1234", role: "institution-provider" </li>
            <li> email: "admin@test.com", password: "1234", role: "institution-admin" </li>
            <li> email: "gov@test.com", password: "1234", role: "gov-verifier" </li>
            <li> email: "super@test.com", password: "1234", role: "super-admin"</li>
        </ul>
      </div>
    </div>
  );
};

// Fake API Call for Demo
const fakeLoginAPI = async (email, password, role) => {
  // Mock data for different roles
  const mockUsers = [
    { email: "provider@test.com", password: "1234", role: "institution-provider" },
    { email: "admin@test.com", password: "1234", role: "institution-admin" },
    { email: "gov@test.com", password: "1234", role: "gov-verifier" },
    { email: "super@test.com", password: "1234", role: "super-admin" },
  ];

  const user = mockUsers.find((u) => u.email === email && u.password === password && u.role === role);
  return user ? { success: true, data: user } : { success: false };
};

export default LoginPage;
