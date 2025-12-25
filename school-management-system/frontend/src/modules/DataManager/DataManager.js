import React, { useState } from 'react';

const DataManager = ({ title }) => {
    const [data, setData] = useState([
        { id: 1, name: 'John Doe' },
        { id: 2, name: 'Jane Smith' },
        { id: 3, name: 'Alice Johnson' },
    ]);
    const [search, setSearch] = useState('');
    const [newItem, setNewItem] = useState('');

    const handleAdd = () => {
        const newId = data.length ? data[data.length - 1].id + 1 : 1;
        const newItemObj = { id: newId, name: newItem };
        setData([...data, newItemObj]);
        setNewItem('');
    };

    const handleDelete = (id) => {
        setData(data.filter((item) => item.id !== id));
    };

    return (
        <div>
            <h1>{title}</h1>
            <input
                type="text"
                placeholder="Search..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {data
                        .filter((item) => item.name.toLowerCase().includes(search.toLowerCase()))
                        .map((item) => (
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.name}</td>
                                <td>
                                    <button onClick={() => handleDelete(item.id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                </tbody>
            </table>
            <input
                type="text"
                placeholder="Add new item"
                value={newItem}
                onChange={(e) => setNewItem(e.target.value)}
            />
            <button onClick={handleAdd}>Add New</button>
        </div>
    );
};

export default DataManager;
