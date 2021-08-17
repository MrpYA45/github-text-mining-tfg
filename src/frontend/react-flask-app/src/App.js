import React from 'react'
import logo from './logo.svg';
import './App.css';
import ListOfRepos from './components/ListOfRepos';

export default function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>GitHub Text Mining</h1>
        <img src={logo} className="App-logo" alt="logo" />
      </header>
        <main>
          <section className="App-add-repo">
            <h2>Añadir Repositorio</h2>
          </section>
          <section className="App-list-repos">
            <h2>Lista de Repositorios Disponibles</h2>
            <ListOfRepos />
          </section>
        </main>

    </div>
  );
}
