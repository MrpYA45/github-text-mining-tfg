import React from 'react';
import './App.css';
import Home from './pages/Home';
import { Route } from 'wouter';

export default function App() {
  return (
    <div className="App">
      <Route
        component={Home}
        path="/"
      />
      <Route
        component={Home}
        path="/user/:user/repo/:repo"
      />
      <Route
        component={Home}
        path="/test"
      />
      <footer className="App-footer">
      &copy; Created by Pablo Fernández
      </footer>
    </div>
  );
}
