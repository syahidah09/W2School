# To update changes of UI files
# pyuic5 -o main_window_ui.py ui/main_window.ui

import datetime
import sys

import psycopg2
import pytz
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QDialog,
                             QListWidget, QListWidgetItem, QMainWindow,
                             QMessageBox)
from PyQt5.uic import loadUi

from main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectDb()

        product = self.loadproduct()
        self.connectSignalsSlots(product)
        self.populateList(product)

    def connectSignalsSlots(self, product):
        cart = []

        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        self.actionEdit_Product.triggered.connect(self.editProduct)
        self.pushButton_4.clicked.connect(self.cardCheck)
        self.pushButton_7.clicked.connect(lambda: self.reset(cart))
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listWidget.setSortingEnabled(True)
        self.listWidget_2.setSortingEnabled(True)

        self.pushButton_2.clicked.connect(
            lambda: self.rmv_cartitem(product, cart))
        self.listWidget_2.itemSelectionChanged.connect(
            lambda: self.cart_change(product, cart))
        self.listWidget.itemSelectionChanged.connect(self.on_change)
        self.pushButton.clicked.connect(
            lambda: self.addToCart(product, cart))
        self.pushButton_3.clicked.connect(lambda: self.clear_cart(cart))
        self.pushButton_6.clicked.connect(
            lambda: self.set_quantity(product, cart))
        self.pushButton_5.clicked.connect(
            lambda: self.confirm_payment(cart, product))
        # If grand total = 0 or '-' and student id = '-' disabled payment button
        self.pushButton_5.setEnabled(False)

    def connectDb(self):
        try:
            self.conn = psycopg2.connect(user="postgres",
                                         password="syida.99",
                                         host="localhost",
                                         port="5432",
                                         database="w2school")
            self.cur = self.conn.cursor()
            print("Successful connection to db")
        except Exception as err:
            print("PostgreSQL Connect() ERROR:", err)

    def update(self):
        self.conn.commit()
        self.populateList(self.loadproduct())

    def editProduct(self):
        dialog = editProductDialog(self)
        dialog.exec()
        self.listWidget.clear()
        self.update()

    def loadproduct(self):
        self.cur.execute(
            "SELECT id,name,price,quantity FROM ewallet_product "
            "WHERE quantity > 0 "
        )
        product = []
        for i in self.cur.fetchall():
            product.append(list(i))
        return product

    def cardCheck(self):
        cardID = self.lineEdit.text()
        # Get student id from card id
        try:
            self.cur.execute(
                "SELECT student_id,first_name, last_name,wallet_balance FROM ewallet_student "
                "WHERE card_id ='{}' ".format(cardID)
            )
            student = self.cur.fetchone()
            print("[cardCheck] student id,name: ", student[0], student[1])
            name = student[1] + " " + student[2]
            self.label_8.setText(str(student[0]))
            self.label_9.setText(name)
            self.pushButton_5.setEnabled(True)
            return student
        except:
            QMessageBox.about(self, "Card Check",
                              "Card is not registered!")

    def about(self):
        QMessageBox.about(
            self,
            "A GUI Application for Co-op/canteen operator",
            "<p>- Can add, update and delete products</p>"
            "<p>- Automatically create order records</p>"
            "<p>- Validate students cards and </p>",
        )

    def populateList(self, product):
        for i in product:
            # print("[populateList] product name: ", i[1])
            item = QListWidgetItem()
            item.setText(i[1])
            self.listWidget.addItem(item)

    def on_change(self):
        print("[on_change] selecteditem: ", [item.text()
              for item in self.listWidget.selectedItems()])

    def addToCart(self, product, cart):
        """
        cart [product_id, name, price, quantity]
        """
        for item in self.listWidget.selectedItems():
            if cart == []:
                self.listWidget_2.addItem(item.text())
                for i in product:
                    if item.text() == i[1]:
                        cart.append([i[0], i[1], i[2],
                                    0])  # dt.strftime("%d/%m/%y")
                        print("[addToCart] '{}' added".format(item.text()))
                        print("[cart]:", cart)
                        break
            else:
                """
                stat will remain False if the item in selectedItem is not in cart
                """
                stat = False
                for j in cart:
                    if item.text() == j[1]:
                        print("[addToCart] message: '{}' already in cart".format(
                            item.text()))
                        stat = True
                        break

                if stat == False:
                    for i in product:
                        if item.text() == i[1]:
                            cart.append([i[0], i[1], i[2],
                                         0])  # dt.strftime("%d/%m/%y")
                            self.listWidget_2.addItem(item.text())
                            print("[cart]:", cart)
                            print("[addToCart] '{}' added".format(item.text()))

    def cart_change(self, product, cart):
        for item in self.listWidget_2.selectedItems():
            # print("[cart_change] item: ", item.text())
            for i in product:
                for j in cart:
                    if item.text() == i[1] and item.text() == j[1]:
                        print("[cart_change] product (id, name): ", i[0], i[1])
                        self.spinBox.setMaximum(i[3])
                        self.label_3.setText(i[1])
                        self.label_15.setText("{:.2f}".format(i[2]))
                        self.spinBox.setValue(j[3])
                        break

    def rmv_cartitem(self, product, cart):
        for item in self.listWidget_2.selectedItems():
            cartitem = self.listWidget_2.currentItem().text()
            print("[rmv_cartitem] selected item:", cartitem)
            for i in product:
                for j in cart:
                    if cartitem == i[1] and cartitem == j[1]:
                        cart.remove(j)
                        print("[rmv_cartitem] item removed:", j)
                        self.listWidget_2.takeItem(self.listWidget_2.row(item))

    def clear_cart(self, cart):
        self.listWidget_2.clear()
        for i in range(len(cart)):
            cart.pop()
        print("[clear_cart] cart:", cart)

    def set_quantity(self, product, cart):
        quantity = self.spinBox.text()
        for i in product:
            for j in cart:
                if self.label_3.text() == i[1] and self.label_3.text() == j[1]:
                    self.spinBox.setValue(j[3])
                    j[3] = int(quantity)
                    print("[set_quantity] item (id, name, quantity): ",
                          i[0], i[1], quantity)
                    print("[set_quantity] cart (name, quantity): ", j[1], j[3])

            gtotal = 0
            items, quantity2, price, total = "", "", "", ""
            for j in cart:
                items += j[1] + " \n"
                quantity2 += str(j[3]) + "\n"
                price += "{:.2f}".format(j[2]) + "\n"
                total += "{:.2f}".format(j[2]*j[3]) + "\n"
                gtotal += j[2]*j[3]
                self.label_22.setText(items)
                self.label_23.setText(quantity2)
                self.label_24.setText(price)
                self.label_11.setText(total)

        print("[cart] grand total:", gtotal)
        self.label_13.setText("{:.2f}".format(gtotal))

    def cart_total(self, cart):
        gtotal = 0
        for j in cart:
            gtotal += j[2]*j[3]
        return gtotal

    def confirm_payment(self, cart, product):
        """
        Create order, orderitem, transaction in db
        Update student wallet balance
        In cart [product_id, name, price, quantity]
        """
        MY = pytz.timezone('Asia/Kuala_Lumpur')
        tm = datetime.datetime.now(MY).timestamp()
        dt = datetime.datetime.now(MY)  # .strftime("%d/%m/%y")
        order_id = str(tm)[:9]
        student = self.cardCheck()

        print("student wallet balance: ", student[3])
        print("cart total: ", self.cart_total(cart))
        # if student has enough balance in wallet
        if student[3] >= self.cart_total(cart):
            print("[cart]:", cart)
            self.cur.execute(
                "INSERT INTO ewallet_order (id, student_id, complete, receive, date_ordered)"
                "VALUES ({},{},{},{},'{}')".format(
                    int(order_id), student[0], True, True, dt)
            )
            self.conn.commit()
            for i in cart:
                # add orderitems for order
                self.cur.execute(
                    "INSERT INTO ewallet_orderitem (order_id, product_id, quantity, date_added) "
                    "VALUES ({},{},{},'{}')".format(
                        int(order_id), i[0], i[3], dt)
                )
                print("[cart_preview] ", i[0], i[1], i[2], i[3])
                for j in product:
                    # update product quantity
                    if i[0] == j[0]:
                        print(
                            "[update_product] name:{}, quantity(stock)={}, quantity(cart)={}".format(i[1], j[3], i[3]))
                        j[3] -= i[3]
                        print(
                            "[update_product] name:{}, quantity(stock)={}".format(i[1], j[3]))
                        self.cur.execute(
                            "UPDATE ewallet_product "
                            "SET quantity={} WHERE id={} ".format(
                                j[3], i[0])
                        )
                        self.conn.commit()

            print("wallet_balance - cart_total=",
                  student[3] - self.cart_total(cart))
            print("student: ", student[0], student[1], student[2], student[3])
            # update student wallet balance
            self.cur.execute(
                "UPDATE ewallet_student "
                "SET wallet_balance={} WHERE student_id={}".format(
                    student[3] - self.cart_total(cart), student[0])
            )
            self.cur.execute(
                "INSERT INTO ewallet_transaction (transaction_id, order_id, student_id, transaction_type, description, amount, date) "
                "VALUES ({},{},{},'Payment','Co-op',{},'{}')".format(
                    tm, int(order_id), student[0], self.cart_total(cart), dt)
            )
            self.conn.commit()
            self.clear_cart(cart)
            self.reset(cart)
            QMessageBox.about(self, "Payment",
                              "Transaction Successful")
        else:
            QMessageBox.about(self, "Payment",
                              "Transaction Denied, not enough balance in wallet")

    def reset(self, cart):
        self.listWidget_2.clear()
        self.clear_cart(cart)
        self.label_3.setText("-")
        self.label_15.setText("-")
        self.label_22.setText("-")
        self.label_23.setText("-")
        self.label_24.setText("-")
        self.label_11.setText("-")
        self.label_13.setText("-")
        self.label_8.setText("-")
        self.label_9.setText("-")
        self.spinBox.setValue(0)
        self.lineEdit.setText("")
        self.pushButton_5.setEnabled(False)


class editProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/update_product.ui", self)
        self.connectDb()
        product = self.loadproduct()
        category = ["School Items", "Stationery", "Workbook", "Food & Drinks"]

        self.pushButton_2.clicked.connect(self.add)
        self.pushButton_3.clicked.connect(lambda: self.update(product))
        self.pushButton_4.clicked.connect(lambda: self.delete(product))
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listWidget.setSortingEnabled(True)
        self.populateList(product)
        self.listWidget.itemSelectionChanged.connect(
            lambda: self.on_change(product, category))
        self.pushButton_5.clicked.connect(self.clear)

        self.comboBox.addItems(category)
        self.comboBox.currentIndexChanged.connect(self.selectionchange)

    def selectionchange(self, i):
        print("Current index", i, "selection changed ",
              self.comboBox.currentText())

    def connectDb(self):
        self.conn = psycopg2.connect(user="postgres",
                                     password="syida.99",
                                     host="localhost",
                                     port="5432",
                                     database="w2school")
        self.cur = self.conn.cursor()

    def loadproduct(self):
        self.cur.execute(
            "SELECT id,name,price,quantity,category FROM ewallet_product "
        )
        product = []
        for i in self.cur.fetchall():
            product.append(list(i))
        return product

    def populateList(self, product):
        print("[populateList] no of products: ".format(len(product)))
        self.label_5.setText("Total no. of products: {} ".format(len(product)))
        for i in product:
            # print("[populateList] product name: ", i[1])
            item = QListWidgetItem()
            item.setText(i[1])
            # print(i[1], i[3])
            if i[3] == 0 or i[3] is None:
                item.setForeground(QColor("#c81313"))
            self.listWidget.addItem(item)

    def on_change(self, product, category):
        for item in self.listWidget.selectedItems():
            for i in product:
                if item.text() == i[1]:
                    self.lineEdit.setText(i[1])
                    self.doubleSpinBox.setValue(i[2])
                    for j in category:
                        if j == i[4]:
                            self.comboBox.setCurrentIndex(category.index(j))
                    if i[3] is None:
                        self.spinBox.setValue(0)
                    else:
                        self.spinBox.setValue(i[3])
                    print("[on_change] selecteditem: ", item.text())
                    break

    def add(self):
        name = self.lineEdit.text()
        price = self.doubleSpinBox.text()
        quantity = self.spinBox.text()
        category2 = self.comboBox.currentText()

        self.cur.execute(
            "INSERT INTO ewallet_product (name, price, quantity, category)"
            "VALUES ('{}',{},{},'{}')".format(name, price, quantity, category2)
        )
        self.listWidget.clear()
        self.populateList(self.loadproduct())
        self.lineEdit.setText("")
        self.doubleSpinBox.setValue(0)
        self.spinBox.setValue(0)
        self.conn.commit()
        QMessageBox.about(self, "Success",
                          "Add New Product Successful")

    def update(self, product):
        for item in self.listWidget.selectedItems():
            for i in product:
                if item.text() == i[1]:
                    i[1] = self.lineEdit.text()
                    i[2] = float(self.doubleSpinBox.text())
                    i[3] = int(self.spinBox.text())
                    i[4] = self.comboBox.currentText()
                    self.cur.execute(
                        "UPDATE ewallet_product "
                        "SET name='{}', price={}, quantity={}, category='{}' WHERE id={}".format(
                            i[1], i[2], i[3], i[4], i[0])
                    )
                    self.conn.commit()
                    print("[update] name='{}', price={}, quantity={}, category='{}' ".format(
                        i[1], i[2], i[3], i[4]))
                    QMessageBox.about(self, "Success",
                                      "Update Product Successful")

    def clear(self):
        self.lineEdit.setText("")
        self.doubleSpinBox.setValue(0)
        self.spinBox.setValue(0)

    def delete(self, product):
        for item in self.listWidget.selectedItems():
            for i in product:
                if item.text() == i[1]:
                    product.remove(i)
                    self.cur.execute(
                        "DELETE FROM ewallet_product WHERE name='{}' ".format(
                            i[1])
                    )
                    self.conn.commit()
                    print("[delete] item: ", )
                    self.listWidget.clear()
                    self.populateList(product)
                    self.lineEdit.setText("")
                    self.doubleSpinBox.setValue(0)
                    self.spinBox.setValue(0)
                    t = "Product named " + i[1] + " deleted successfully"
                    QMessageBox.about(self, "Success",t)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Window()
    win.show()
    sys.exit(app.exec())
