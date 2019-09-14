#! /usr/bin/env python3

# This file is a part of NUMCL project.
# Copyright (c) 2019 IBM Corporation
# SPDX-License-Identifier: LGPL-3.0-or-later
# 
# NUMCL is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any
# later version.
# 
# NUMCL is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# NUMCL.  If not, see <http://www.gnu.org/licenses/>.

from numpy import *
from benchmarker import Benchmarker

loop = 100

with Benchmarker(loop, width=20) as bench:

    a = zeros((1000,1000))
    b = zeros((1000,1000))
    c = zeros((1000,1000))
    b2 = zeros((30,30))
    c2 = zeros((30,30))
    
    @bench('einsum_gemm')
    def run_einsum_gemm(bm):
        for i in bm:
            einsum('ij,jk->ik',a,b,out=c)
    
    @bench('builtin_gemm')
    def run_builtin_gemm(bm):
        for i in bm:
            matmul(a,b,out=c)