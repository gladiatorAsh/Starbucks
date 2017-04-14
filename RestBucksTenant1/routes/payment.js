var Orders = require('../models/order');
var ObjectId = require('mongoose').Types.ObjectId;

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

exports.makePayment = makePayment;