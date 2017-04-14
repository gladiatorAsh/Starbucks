var Orders = require('../models/order');
var ObjectId = require('mongoose').Types.ObjectId;

var getAllOrders = function(req, res) {

	Orders.find({}, function(err, orders) {
		if (err) {
			res.status(500).send();
			throw err;
		}

		if (orders === undefined) {
			res.status(404).send();
		} else {
			res.status(200).send(orders);
		}
	});
};

exports.getAllOrders = getAllOrders;
