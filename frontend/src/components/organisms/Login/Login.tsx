import React, { useState } from 'react'
import axios from 'axios'

import './style.scss'
import { useNavigate } from 'react-router-dom'

export const Login = () => {

  const navigate = useNavigate();

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [formError, setFormError] = useState(false)

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const payload_api = {
      "email": email,
      "password": password,
    }
    axios.post("http://127.0.0.1:8000/login", payload_api)
      .then(function (response) {
        if (response.data.message.includes('Authenticated')) {
          console.log('logging success!')
          setFormError(false)
          localStorage.setItem("Authorization", "true")
          navigate("/");

        } else {
          localStorage.setItem("Authorization", "false")
          setFormError(true)
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  return (
    <div className='logging-container'>
      <h1>Welcome</h1>
      <p></p>
      <form onSubmit={(event) => handleSubmit(event)} className='logging-input'>
        <input type="email"
          onChange={(e) => setEmail(e.target.value)}
          value={email}
          placeholder='Email'
        />
        <input type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder='Password'
        />

        {formError && <p>verifica tu email o contraseña</p>}
        <button type='submit' className='button-submit'>Log in</button>
      </form>
    </div>
  )
}

export default Login