# CUDA 확장을 빌드하기 위한 setup 스크립트
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

setup(
    name='bitlinear_cpp',
    ext_modules=[
        CUDAExtension('bitlinear_cuda', [
            'bitnet_kernels.cu',
        ])
    ],
    cmdclass={
        'build_ext': BuildExtension
    })