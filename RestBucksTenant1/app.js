var express = require('express')
, http = require('http')
, path = require('path');

var order = require('./routes/order')
var orders = require('./routes/orders')
var payment = require('./routes/payment')

var app = express();

// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
	app.use(express.errorHandler());
}

// get request
app.get('/orders/:id', order.getOrder);
app.get('/orders', orders.getAllOrders);

// post request
app.post('/orders', order.newOrder);
app.post('/orders/:id/pay', payment.makePayment);

// put request
app.put('/orders/:id', order.updateOrder);

// delete request
app.del('/orders/:id', order.deleteOrder);

http.createServer(app).listen(app.get('port'), function() {
	console.log('Express server listening on port ' + app.get('port'));
});