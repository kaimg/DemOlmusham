import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
//npm create vite@latest my-project -- --template react
//npm install -D tailwindcss postcss@8.1
//npx tailwindcss -i ./src/index.css -o ./src/style.css --watch 
//npm install -D tailwindcss@3.0.24 postcss@8.4.5 autoprefixer@10.4.2
