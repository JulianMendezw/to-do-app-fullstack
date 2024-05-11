import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ToDoList from './components/organisms/ToDoList/ToDoList';
import { ProtectedRoute } from './components/ProtectedRoute';
import Login from './components/organisms/Login/Login';

import './App.scss';

function App() {

  return (
    <div className="App">
      <Router>
        <Routes >
          <Route index path="/" element={
            <ProtectedRoute>
              <ToDoList />
            </ProtectedRoute>
          } />
          <Route path="/login" Component={Login} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
