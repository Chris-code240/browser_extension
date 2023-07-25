
  let videos = document.querySelectorAll('video')
  videos.forEach((video, index)=>{
    fetch('http://localhost:5000/analyze',{
      body:JSON.stringify({"path":video.src}),
      headers: {"Content-type":"application/json"},
      method: "POST"
    }).then((res)=>res.json()).then((jres)=>{
      if(jres.success && jres.trigger){
        video.parentElement.classList.add('hidden')

      }
    }).catch((e)=>console.log(e))

    if(index + 1 == videos.length){
      let con = confirm("Some content are possible epileptic triggers. Do you want to see them anyway?")
      if (con){
        videos.forEach(video=>{
          if(video.parentElement.classList.contains('hidden')){
            video.parentElement.classList.remove('hidden')
          }
        })
      }
    }
  })


