import React, { useState } from 'react'
import axios from 'axios'

import './style.scss'
import { useNavigate } from 'react-router-dom'

export const Login = () => {

  const navigate = useNavigate();

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [formError, setFormError] = useState(false)
  const [textError, setTextError] = useState('')

  const getData = async () => {
    try {
      const headers = { "Content-Type": "application/x-www-form-urlencoded" }
      const payload = {
        "username": email, "password": password,
      }

      const response = await axios.post(
        `http://127.0.0.1:8000/token`,
        payload,
        { headers }
      );
      localStorage.setItem("Authorization", "true")
      navigate("/");

    } catch (error: any) {
      console.log(error)
      localStorage.setItem("Authorization", "false")
      setTextError(error.response.data.detail)
      setFormError(true)
    }
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    getData()
  }

  return (
    <div className='logging-container'>
      <h1>Welcome</h1>
      <p></p>
      <form onSubmit={(event) => handleSubmit(event)} className='logging-input'>
        <input type="text"
          onChange={(e) => setEmail(e.target.value)}
          value={email}
          placeholder='User'
        />
        <input type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder='Password'
        />

        {formError && <p>{textError}</p>}
        <button type='submit' className='button-submit'>Log in</button>
      </form>
    </div>
  )
}

export default Login