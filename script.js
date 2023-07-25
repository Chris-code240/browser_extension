
  let videos = document.querySelectorAll('video')
  let images = document.querySelectorAll('img')
  let contents = document.querySelectorAll('img, video')
  let counter = 0
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

  contents.forEach((ele, index)=>{
    if(ele.tagName == "img"){
      fetch('http://localhost:5000/analyze-image',{
        body:JSON.stringify({"path":ele.src}),
        headers: {"Content-type":"application/json"},
        method: "POST"
      }).then((res)=>res.json()).then((jres)=>{
        if(jres.success && jres.trigger){
          ele.parentElement.classList.add('hidden')
          counter += 1
        }
      }).catch((e)=>console.log(e))
    }else{
      fetch('http://localhost:5000/analyze',{
        body:JSON.stringify({"path":ele.src}),
        headers: {"Content-type":"application/json"},
        method: "POST"
      }).then((res)=>res.json()).then((jres)=>{
        if(jres.success && jres.trigger){
          ele.parentElement.classList.add('hidden')
          counter += 1
        }
      }).catch((e)=>console.log(e))      
    }

    if(index + 1 == videos.length && counter > 0){
      let con = confirm("Some content are possible epileptic triggers. Do you want to see them anyway?")
      if (con){
        contents.forEach(ele=>{
          if(ele.parentElement.classList.contains('hidden')){
            ele.parentElement.classList.remove('hidden')
          }
        })
      }
    }
  })


