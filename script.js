
  console.log("Loading..")
  let videos = document.querySelectorAll('video')
  
  videos.forEach(video =>{
    fetch('http://localhost:5000/analyze',{
      body:JSON.stringify({"path":video.src}),
      headers: {"Content-type":"application/json"},
      method: "POST"
    }).then((res)=>res.json()).then((jres)=>{
      console.log(jres)
    }).catch((e)=>console.log(e))
  })
