
function clickEventHandler (isKeras) {
  let image = document.getElementById('input_image')
  if (image.files.length === 0) {
    alert('Please upload a file')
    return
  }

  let spanId = 'result-span'
  if (isKeras) spanId = 'result-keras'
  document.getElementById(spanId).innerHTML = 'Loading...'

  let fd = new FormData()
  fd.append('input_image', image.files[0])

  let request = new XMLHttpRequest();
  let target = '/'
  if (isKeras) target = '/keras'
  request.open('POST', target, true);

  if (isKeras) request.responseType = 'text';
  else request.responseType = 'blob';

  request.onreadystatechange = () => {
    if (request.status === 200 && request.readyState == XMLHttpRequest.DONE) {
      document.getElementById(spanId).innerHTML = ''
      if (isKeras) {
        document.getElementById('result-keras').innerHTML = request.response
        // let urlCreator = window.URL || window.webkitURL
        // let imageURL = urlCreator.createObjectURL(request.response)
        // document.getElementById('result-keras').src = imageURL
        return
      }

      let urlCreator = window.URL || window.webkitURL
      let imageURL = urlCreator.createObjectURL(request.response)
      document.getElementById('result').src = imageURL
    }
  }
  request.send(fd);
}

let submitButton = document.getElementById('submit')
submitButton.addEventListener('click', () => {
  clickEventHandler(false)
})

let submitKerasButton = document.getElementById('submit-keras')
submitKerasButton.addEventListener('click', () => {
  clickEventHandler(true)
})
