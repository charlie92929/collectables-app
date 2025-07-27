import React, { useState } from 'react'
export default function Uploads() {
    const [name, setName] = useState("")
    const [desc, setDesc] = useState("")
    const [tags, setTags] = useState("")
    const [image, setImage] = useState(null)
    const [message, setMessage] = useState("")

    const handleSubmit = async e => {
        e.preventDefault()
        const formData = new FormData()
        formData.append('name', name)
        formData.append('description',desc)
        formData.append('tags',tags)
        formData.append('image',image)

        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        })

        const data = await response.json()
        console.log(data)
        setMessage(data.message)
    }


    return(
        <div>
            <form onSubmit={handleSubmit} encType='multipart/form-data'>
                <input
                    placeholder='Name'
                    value={name}
                    onChange={e => setName(e.target.value)}
                    required
                />
                <input
                    placeholder='desc'
                    value={desc}
                    onChange={e => setDesc(e.target.value)}
                    required
                />
                <input
                    placeholder='tags'
                    value={tags}
                    onChange={e => setTags(e.target.value)}
                    required
                />
                <input
                    type='file'
                    accept='image/*'
                    onChange={e => setImage(e.target.files[0])}
                />
                <button type="submit">Upload</button>
            </form>
            <p>{message}</p>
        </div>
    )
}