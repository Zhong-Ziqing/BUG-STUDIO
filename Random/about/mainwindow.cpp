#include "mainwindow.h"
#include "ui_mainwindow.h"
#include<QPalette>
#include<QLabel>
#include<QImage>
#include<QMouseEvent>
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setFixedSize(1400,950);
    this->setWindowTitle("About");
    this->setWindowIcon(QIcon(":/icon.png"));
    this->setWindowFlags(Qt::Dialog | Qt::FramelessWindowHint);
    this->setAttribute(Qt::WA_TranslucentBackground, true);
    ui->label->resize(this->size());
    QImage image;
    image.load(":/about.png");
    ui->label->setPixmap(QPixmap::fromImage(image));
    ui->label->resize(QSize(image.width(),image.height()));
}
MainWindow::~MainWindow()
{
    delete ui;
}
