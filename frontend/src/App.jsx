import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import PostsPage from "./pages/PostsPage";

function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<LoginPage />}
        />

        <Route
          path="/posts"
          element={<PostsPage />}
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;