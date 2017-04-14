var Orders = require('../models/order');
var ObjectId = require('mongoose').Types.ObjectId;

var getOrder = function(req, res) {
	var orderID = req.param("id");

	Orders.findById(orderID, function(err, order) {
		if (err) {
			res.status(500).send();
			throw err;
		}
		if (order === null) {
			res.status(404).send();
		} else {
			res.status(200).send(order);
		}
	});
};

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

var newOrder = function(req, res) {

	var orderDetails = req.body;

	if (orderDetails.location === undefined || orderDetails.items === undefined) {
		res.status(400).send(orderDetails);
	} else {
		if (orderDetails.items !== undefined) {
			var flag = 0;
			
			var items = orderDetails.items;
			for (var i = 0; i < items.length; i++) {

				if (items[i].size === undefined || items[i].name === undefined
						|| items[i].qty === undefined
						|| items[i].milk === undefined) {
					flag = 1;
				}
			}
		
			if (flag === 0) {
				orderDetails.status = "PLACED";
				orderDetails.message = "Your order has been placed";

				var order = new Orders(orderDetails);
				order.save(function(err) {
					if (err) {
						res.status(500).send();
						throw err;
					} else {
						res.location('http://localhost:3000/orders/' + order._id);
						res.status(201).send(order);
					}
				});
			} else {
				res.status(400).send(orderDetails);
			}
		}
	}
};

var makePayment = function(req, res) {

	var orderID = req.param("id");
	Orders.findById(orderID, function(err, order) {
		console.log(order);
		if (err) {
			res.status(500).send();
			throw err;
		}

		if (order === null) {
			res.status(404).send();
		} else if (order.status === "PLACED") {
			order.message = "PAYMENT ACCEPTED";
			order.status = "PAID";
			order.save(function(err) {
				if (err) {
					res.status(500).send();
				} else {
					res.status(200).send(order);
				}
			});
		} else {
			res.status(412).send();
		}
	});
};

var updateOrder = function(req, res) {

	var orderID = req.param("id");
	var orderDetails = req.body;

	Orders.findById(orderID, function(err, order) {

		if (order === undefined || order.status !== "PLACED") {
			res.status(412).send();

		} else {

			console.log(order);
			order.location = orderDetails.location;
			order.items = orderDetails.items;
			order.status = "PREPARING";

			order.save(function(err) {
				if (err) {
					res.status(500).send();
					throw err;
				} else {
					res.status(200).send(order);
				}
			});
		}
	});
};

var deleteOrder = function(req, res) {

	var orderID = req.param("id");
	Orders.findById(orderID, function(err, order) {
		if (err) {
			res.status(500).send();
			throw err;
		}

		if (order === undefined || order === null) {
			res.status(404).send();
		} else {
			order.remove(function(err) {
				if (err) {
					throw err;
				} else {
					res.status(204).send();
				}
			});
		}
	});
};

exports.getOrder = getOrder;
exports.getAllOrders = getAllOrders;
exports.newOrder = newOrder;
exports.makePayment = makePayment;
exports.updateOrder = updateOrder;
exports.deleteOrder = deleteOrder;