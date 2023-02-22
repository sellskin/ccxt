'use strict'

const testBorrowRate = require ('./test.borrowRate.js');

async function testFetchBorrowRate (exchange, code) {
    const method = 'fetchBorrowRate';
    const skippedExchanges = [];
    if (exchange.inArray(exchange.id, skippedExchanges)) {
        console.log (exchange.id, method, 'found in ignored exchanges, skipping ...');
        return;
    }
    let borrowRate = undefined;
    try {
        borrowRate = await exchange[method] (code);
    } catch (ex) {
        const message = ex.message;
        // for exchanges, atm, we don't have the correct lists of currencies, which currency is borrowable and which not. So, because of our predetermined list of test-currencies, some of them might not be borrowable, and thus throws exception. However, we shouldn't break tests for that specific exceptions, and skip those occasions.
        if (message.indexOf ('could not find the borrow rate for currency code') < 0) {
            throw new Error (message);
        }
        // console.log (method + '() : ' + code + ' is not borrowable for this exchange. Skipping the test method.');
        return;
    }
    console.log (exchange.id, method, 'fetched succesfully, asserting now ...');
    testBorrowRate (exchange, method, borrowRate, code);
}

module.exports = testFetchBorrowRate;