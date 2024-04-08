import React, { useState, useEffect } from 'react';
import './App.css';
import logo from './rocketweb.svg';
/*import { getDataFromDynamoDB } from './dynamoDBService';*/

const data = [
  { id: '1', title: 'Rocket 1', payload: 'Word 1', company: 'Space X', details: 'today' },
  { id: '2', title: 'Rocket 2', payload: 'Word 2', company: 'NASA', details: 'tomorrow' },
  { id: '3', title: 'Rocket 3', payload: 'Word 3', company: 'Space X', details: 'tonight' }
];

function App() {/*
  const [data, setData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const items = await getDataFromDynamoDB();
        setData(items);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }

    fetchData();
  }, []);
*/
  return (
    <div className="App">
      <nav className="navbar">
        <div className="navbar-brand">
            <img src={logo} alt="Logo" className="navbar-logo" />
            <h1 className="navbar-title">Rocket Web</h1>
        </div>
      </nav>
      <div className="list-container">
        {data.map(item => (
          <div key={item.id} className="list-item">
            <h2>{item.title}</h2>
            <p><strong>Payload:</strong> {item.payload}</p>
            <p><strong>Company:</strong> {item.company}</p>
            <p><strong>Details:</strong> {item.details}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
