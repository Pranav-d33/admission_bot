import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import SuperAdminDashboard from "./components/SuperAdminDashboard";
import GovVerifierDashboard from "./components/GovVerifierDashboard";
import InstitutionAdminDashboard from "./components/InstitutionAdminDashboard";
import InstitutionProviderDashboard from "./components/InstitutionProviderDashboard";
import LoginPage from "./components/LoginPage";

function PrivateRoute({ element, role }) {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/" />;
  }

  if (user.role !== role) {
    return <Navigate to="/" />;
  }

  return element;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route
          path="/super-admin"
          element={
            <PrivateRoute
              element={<SuperAdminDashboard />}
              role="super-admin"
            />
          }
        />
        <Route
          path="/gov-verifier"
          element={
            <PrivateRoute
              element={<GovVerifierDashboard />}
              role="gov-verifier"
            />
          }
        />
        <Route
          path="/institution-admin"
          element={
            <PrivateRoute
              element={<InstitutionAdminDashboard />}
              role="institution-admin"
            />
          }
        />
        <Route
          path="/institution-provider"
          element={
            <PrivateRoute
              element={<InstitutionProviderDashboard />}
              role="institution-provider"
            />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;

// import FloatingChatbot from './components/FloatingChatbot';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       {/* Main application content can go here */}
//       <FloatingChatbot />
//     </div>
//   );
// }
