import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [articulos, setArticulos] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/articulos/')
      .then(response => setArticulos(response.data))
      .catch(error => console.error('There was an error fetching the articles!', error));
  }, []);

  return (
    <div>
      <h1>Mi Blog</h1>
      <ul>
        {articulos.map(articulo => (
          <li key={articulo.id}>{articulo.titulo}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
