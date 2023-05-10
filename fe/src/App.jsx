import { useState } from "react"
import "./app.css"
import "./loading.css"
import "./button.css"

function App() {
  const [predict, setPredict] = useState("input the massage")
  const [text, setText] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const onSubmit = () => {
    fetch('http://127.0.0.1:8000', {
      method: "POST",
      headers:{
        'Content-Type': 'application/json',
      } ,
      body: JSON.stringify({txt:text})
    })
    .then(res => res.json())
    .then(data => setPredict(data["txt"]))
    .then(() => setIsLoading(false))
  }

  const loadingSpin = () => {
    return <div className="lds-dual-ring"></div>
  }

  const comSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);
    onSubmit();
  }

  return (
    <div>
      <nav>
        <h3>Sentiment Analyst Project</h3>
      </nav>
      <div className="pd">
        <div>
          {isLoading?loadingSpin() : predict}
        </div>
      </div>
      <div className="formInput">
        <form onSubmit={comSubmit}>
          <textarea name="txt" cols="30" rows="10" value={text} onChange={e => setText(e.target.value)}></textarea><br />
          <div className="container">
            <button type="submit">submit</button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default App
