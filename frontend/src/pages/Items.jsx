import React, { useState, useEffect } from 'react'
export default function Items() {
    const [items, setItems] = useState([])

    useEffect(() => {
        fetch('http://127.0.0.1:5000/items')
         .then(res => res.json())
         .then(data => setItems(data))
         // allows us to sucessfully update the state of items on a request
         .catch(err => {
            console.error(err)
         }
         )
    }, [])


    return (
        <div>
            <ul>
                {items.map((item, i) => (
                    <li key={i}>
                        <strong>{item.name}</strong>
                        <p>{item.desc}</p>
                        {item.tags?.length > 0 && <p>Tags: {item.tags.join(', ')}</p>}
                        {item.image && (
                            <img
                                src={`http://127.0.0.1:5000${item.image}`}
                                alt={item.name}
                                width="150"
                            />
                        )}
                    </li>
                ))}
            </ul>
        </div>
    )
}