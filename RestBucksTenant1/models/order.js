var mongoose = require('mongoose');
mongoose.connect('mongodb://localhost:27017/restbucks');

var Schema = mongoose.Schema;

var orderSchema = new Schema({

	location : String,
	items : Array,
	status : String,
	message : String,
});

orderSchema.methods.updateStatus = function(status){
	this.status = status;
	return this.status;
};




var Order = mongoose.model('Order', orderSchema);

module.exports = Order;