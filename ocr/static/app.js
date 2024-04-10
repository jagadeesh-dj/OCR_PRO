
    // function search(){
    //     const bundle=[]
    //     let searchbox=document.getElementById('search')
    //     let list=document.querySelectorAll('#filename > p')
    //     list.forEach(val=>{
    //         bundle.append(val)
    //     })
    //     console.log(bundle)
        

    // }
    // search();
    function dropdown_button(){

        let icon=document.querySelectorAll('#list')
        icon.forEach((item)=>{
            item.addEventListener('click',(e)=>{
                let menus=document.querySelectorAll('#list-menu')
                menus.forEach((down)=>{
                    if (down.parentElement.getAttribute('id')==e.target.getAttribute('value'))
                    down.classList.toggle('hidden2')
                })
            })
        })
    }
    dropdown_button();


        function txtfile(){
            let file=document.getElementById('fileslist')
            let mylist=document.getElementById('my_list')
            fetch('http://127.0.0.1:8000/fileview/',{
                method:'GET'
            })
            .then(res=>res.json())
            .then(data=>{
                // data.forEach((files)=>{
                //     let ht=`<div id="${ files.id }">\
                //                     <li>\
                //                         <div id="filename">\
                //                             <p>"${ files.name }"</p>\
                //                         </div>\
                //                         <div id="icons">\
                //                             <i class="fa-solid fa-caret-down fa-lg" style="color: #fcf8fa;" value="${ files.id }" id="list"></i>\
                //                         </div>\
                //                     </li>\
                //                     <div id="list-menu" class="hidden2">\
                //                         <div id="download">\
                //                             <a href="{% url "download" file_name="${files.name}" %}"><p>Download</p></a>\
                //                         </div>\
                //                         <div id="delete">\
                //                             <a href="{% url "delete" file_name="${files.name}" %}"><p>Delete</p></a>\
                //                         </div>\
                //                     </div>\
                //                 </div>`
                //     mylist.appendChild(ht)
                let div1=document.createElement('div')
                div1.setAttribute('id',data.id)
                let div2=document.createElement('div')
                let div3=document.createElement('div')
                div2.setAttribute('id','filename')
                div3.setAttribute('id','icons')
                let p=document.createElement('p')
                let i=document.createElement('i')
                p.innerText=data.name
                i.setAttribute('class',"fa-solid fa-caret-down fa-lg")
                i.setAttribute('value',data.id)
                i.setAttribute('id','list')
                i.style.color='#fcf8fa'
                div2.appendChild(p)
                div3.appendChild(i)
                let list=document.createElement('li')
                list.appendChild(div2)
                list.appendChild(div3)
                div1.appendChild(list)

                let div4=document.createElement('div')
                div4.setAttribute('id','list-menu')
                div4.setAttribute('class','hidden2')

                let div5=document.createElement('div')
                div5.setAttribute('id','download')
                let p2=document.createElement('p')
                p2.innerText='Download'
                
                div5.appendChild(p2)

                let div6=document.createElement('div')
                div6.setAttribute('id','delete')
                let p3=document.createElement('p')
                p3.innerText='Delete'

                div6.appendChild(p3)
                div4.appendChild(div5)
                div4.appendChild(div6)
                div1.appendChild(div4)
                mylist.appendChild(div1)
                let file_name=data.name
                console.log(file_name)
                dropdown_button()      
                p2.addEventListener('click',(e)=>{
                    var url='/download/'+file_name
                    window.location.href=url
                })  
                p3.addEventListener('click',(e)=>{
                    var url1='/delete/'+file_name
                    window.location.href=url1
                })
            })
            dropdown_button()
            // document.getElementById('duplicate').addEventListener('click',(e)=>{
            //     fetch('download/file_name='+`${data.name}`+'/',{
            //     method:'GET'
            //     })
            // })
               
        }
        // setInterval(txtfile,1000);
    function delete_txt_file(){
        let del=document.getElementById('delete')
        del.addEventListener('click',(e)=>{
            e.addEventListener();
        })
    }

    // upload a file to the backend
    function uploadfiles(){

        let upload=document.getElementById('files')
        upload.addEventListener('change',(e)=>{
            document.querySelector('textarea').innerText="LODING PLEASE WAIT!....."

            let csrf=document.querySelector('[name=csrfmiddlewaretoken]').value;
    
            let file=e.target.files[0]
            const form=new FormData()
            form.append('files',file)
    
            fetch('http://127.0.0.1:8000/upload/',{
                method:'POST',
                headers:{
                    "X-CSRFToken":csrf,
                },
                body: form
            })
            .then(res=>res.json())
            .then(data => {
                console.log('File uploaded successfully');
                data.forEach((val)=>{
                    console.log('recieved',val)
                    document.querySelector('textarea').innerText=val.data
                })
                    
            })
        })
    }
    uploadfiles();

    //fetching the predicted data to display in textarea 
  
    
    // clear data in the teaxarea
    function clear(){
        let mic=document.getElementById('mic')
        let pause=document.getElementById('pause')
        let clear=document.getElementById('clean')
        let textarea=document.querySelector('textarea')
        clear.addEventListener('click',(e)=>{
            textarea.innerText=''
            window.speechSynthesis.cancel();
            mic.classList.remove('hidden')
            pause.classList.add('hidden')
        })
    }
    clear();

    // audio generator
    function audio(){

        let mic=document.getElementById('mic')
        let pause=document.getElementById('pause')
        let speak=document.getElementById('speak')
        let pass=document.getElementById('pass')
        let textarea=document.querySelector('textarea')

        speak.addEventListener('click',(e)=>{

            var utterance = new SpeechSynthesisUtterance(textarea.value);
    
            var voices = window.speechSynthesis.getVoices();
            utterance.voice = voices.find(v => v.lang === 'en-US');

          

            utterance.onend = function end(event) {
                mic.classList.remove('hidden')
                pause.classList.add('hidden')
            };
            
            window.speechSynthesis.speak(utterance);
            
        })
            
     
        speak.addEventListener('click',()=>{
            mic.classList.add('hidden')
            pause.classList.remove('hidden')
        })
        pass.addEventListener('click',()=>{
            window.speechSynthesis.cancel()
            mic.classList.remove('hidden')
            pause.classList.add('hidden')
        })
    }
    audio();
 
  
    // save the predicted data as txt file
    function save_txt_file(){

        let textarea=document.querySelector('textarea')
        let save=document.getElementById('save')
        let clickcount=0
     
        save.addEventListener('click',(e)=>{
             clickcount++;
     
             console.log(clickcount)
             if (textarea.value != ""){
                 files_names=prompt('enter file name: ')
                 console.log(files_names)
                 let fileform=new FormData()
                 fileform.append('content',textarea.value)
                 fileform.append('file_name',files_names)
                 fetch('http://127.0.0.1:8000/txtfile/',{
                     method:'POST',
                     headers:{
                         'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                     },
                     body: fileform
                 })
                 .then(response => {
                    if (response.ok) {
                         // Handle success
                        console.log('File saved successfully');
                        txtfile();
                        delete_txt_file();
                         
                    }else {
                         // Handle error
                         console.error('Error uploading file');
                     }
                 })
                 .catch(error => {
                     console.error('Error:', error);
                 });
             }
             return
        })
    }
    save_txt_file();
   
    function edit_txt_file(){
        let edit=document.querySelectorAll('#edit')
        edit.forEach(ele=>{
            ele.addEventListener('click',(e)=>{
                e.preventDefault();
                console.log('clicked')
                document.querySelector('textarea').innerText=""
    
                let name=ele.querySelector('a').getAttribute('value')
                fetch('http://127.0.0.1:8000/edit/'+name+'/',{
                    method:'GET',
                    headers:{
                        'Content-Type':'application/json'
                    }
                })
                .then(res=>res.json())
                .then(data=>{
                    data.forEach((item)=>{
                        document.querySelector('textarea').innerText=item.content
                        // console.log(item.content)
                    })
                })
            })
        })
    }
    edit_txt_file();