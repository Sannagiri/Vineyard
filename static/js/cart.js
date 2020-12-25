var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var brandId = this.dataset.brand
		var action = this.dataset.action
        console.log('brandId:', brandId, 'Action:', action)
        
		console.log('USER:', user)
		if (user == 'AnonymousUser'){
			console.log('User is not authenticated')
			
        }
        else{
			updateUserOrder(brandId, action)
		}
	})
}

function updateUserOrder(brandId,action){
	console.log('User is authenticated, sending data...')

	var url ='/updateitem/'

	fetch(url, {
		method :'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'brandId':brandId,'action':action})
	})

	.then((response) =>{
		return response.json()	
	})
	.then((data) =>{

		location.reload()	
	})
}