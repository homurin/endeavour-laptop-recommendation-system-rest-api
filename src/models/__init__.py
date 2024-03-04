from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, VARCHAR
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from src.models import db


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(Base)


class Laptop(db.Model):
    __tablename__ = "Laptop"
    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    # brandId: Mapped[str] = mapped_column(VARCHAR(36), ForeignKey("Brand.id"))
    cpuId: Mapped[str] = mapped_column(VARCHAR(36), ForeignKey("Cpu.id"))
    gpuId: Mapped[str] = mapped_column(VARCHAR(36), ForeignKey("Gpu.id"))
    winId: Mapped[str] = mapped_column(
        VARCHAR(36),  ForeignKey("Windows.id"))
    name: Mapped[str] = mapped_column(VARCHAR(255))
    cpu: Mapped["Cpu"] = relationship(back_populates="laptops")
    gpu: Mapped["Gpu"] = relationship(back_populates="laptops")
    windows: Mapped["Windows"] = relationship(back_populates="laptops")
    # brand: Mapped["Brand"] = relationship(back_populates="laptops")
    osEdition: Mapped[str]
    thumb: Mapped[str]
    price: Mapped[float] = mapped_column(MONEY)
    ram: Mapped[float]
    ssdStorage: Mapped[float]
    hddStorage: Mapped[float]
    # displaySize: Mapped[int]
    # displayResolution: Mapped[str] = mapped_column(VARCHAR(50))
    # displayName: Mapped[str] = mapped_column(VARCHAR(50))
    # panelType: Mapped[str]
    # panelCode: Mapped[int]
    # refreshRate: Mapped[int]
    # weight: Mapped[float]


class Cpu(db.Model):
    __tablename__ = "Cpu"
    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50))
    baseSpeed: Mapped[float]
    maxSpeed: Mapped[float]
    cores: Mapped[int]
    threads: Mapped[int]
    laptops: Mapped[List["Laptop"]] = relationship(back_populates="cpu")


class Gpu(db.Model):
    __tablename__ = "Gpu"
    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50))
    maxSpeed: Mapped[float]
    directX: Mapped[float]
    openGl: Mapped[float]
    memory: Mapped[float]
    memorySpeed: Mapped[float]
    laptops: Mapped[List["Laptop"]] = relationship(back_populates="gpu")


class Windows(db.Model):
    __tablename__ = "Windows"
    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50))
    buildNumber: Mapped[int]
    laptops: Mapped[List["Laptop"]] = relationship(back_populates="windows")
    applications: Mapped[List["Application"]] = relationship(
        back_populates="windows")


# class Brand(db.Model):
#     __tablename__ = "Brand"
#     id: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True)
#     name: Mapped[str] = mapped_column(VARCHAR(50))
#     laptops: Mapped[List["Laptop"]] = relationship(back_populates="brand")


class Application(db.Model):
    __tablename__ = "Application"
    id: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    winId: Mapped[str] = mapped_column(VARCHAR(36), ForeignKey("Windows.id"))
    name: Mapped[str] = mapped_column(VARCHAR(100))
    minCpuSpeed: Mapped[float]
    minCores: Mapped[int]
    minThreads: Mapped[int]
    minGpuBoostClock: Mapped[float]
    minGpuMemory: Mapped[float]
    minDirectX: Mapped[float]
    minOpenGl: Mapped[float]
    minRam: Mapped[float]
    minStorage: Mapped[float]
    windows: Mapped["Windows"] = relationship(back_populates="applications")
