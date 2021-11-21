// let scan_img = document.getElementById('scan')

console.log('wwigfyguhioqpekowfhbfwijdoevh');

function open_file(){
    document.getElementById('input_file').click();
}


scan_img = function(event){
    // console.log(document.getElementById('input_file').value);
        let search_img = document.getElementById('search_img');
        search_img.src = URL.createObjectURL(event.target.files[0]);


        let scan_img = document.getElementById('scan_search')

        scan_img.style.marginLeft = '210px'
        caption = document.querySelector('.caption')
        if(caption){
            caption.innerHTML = ""
        }
        // document.forms['img_sum_form'].submit()
        
        // scan_img_req(formData)   

        const fileInput = document.querySelector('#input_file')
        const formData = new FormData()

        formData.append('file',fileInput.files[0]);
        const csrftoken = getCookie('csrftoken');
        const options = {
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-CSRFToken':csrftoken
            },
            body:formData,
        }
        scan_img_req(options)
    
}





function scan_img_req(options){
    // console.log(img.src);
    

    const url = 'http://127.0.0.1:8000/process_img'

    let caption_div = document.querySelector('.caption')

    console.log('fdeidfhuiehfhuewh');
    
    let loader = document.getElementById('scan_id_load')
    loader.className = 'scan'
    // console.log(    );
    loader.childNodes[1].id = 'scan_id'
    


    
    

    
     
    
    
    fetch(url,options)
    .then(response =>{
        return response.json()
    })
    .then(data => {
        console.log(data);
        caption_div.innerHTML = data['caption']
        loader.className = ""
        loader.id = 'scan_id_load'
        loader.childNodes[1].id = ''
    })
}





function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
