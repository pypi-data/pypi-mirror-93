/*******************************************************************************
* Copyright 2020 Intel Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#ifndef CPU_X64_JIT_AVX512_CORE_AMX_CONV_KERNEL_HPP
#define CPU_X64_JIT_AVX512_CORE_AMX_CONV_KERNEL_HPP

#include "common/c_types_map.hpp"
#include "common/memory_tracking.hpp"

#include "cpu/x64/jit_avx512_core_amx_tilecfg.hpp"
#include "cpu/x64/jit_generator.hpp"
#include "cpu/x64/jit_primitive_conf.hpp"
#include "cpu/x64/jit_uni_eltwise_injector.hpp"

namespace dnnl {
namespace impl {
namespace cpu {
namespace x64 {

struct jit_avx512_core_amx_copy_to_pbuffer_t : public jit_generator {
    DECLARE_CPU_JIT_AUX_FUNCTIONS(jit_avx512_core_amx_copy_to_pbuffer_t)

    using reg64_t = const Xbyak::Reg64;

    jit_avx512_core_amx_copy_to_pbuffer_t(jit_conv_conf_t ajcp) : jcp(ajcp) {
        generate();
    }

private:
    jit_conv_conf_t jcp;

    const reg64_t inp_ptr = r15;
    const reg64_t out_ptr = r14;

    const reg64_t khp = r13;
    const reg64_t khc = r12;

    const reg64_t aux_inp_ptr = r11;
    const reg64_t aux_out_ptr = r10;
    const reg64_t reg_icb = r9;

    const reg64_t kh_over = r8;
    const reg64_t tover = rax;
    const reg64_t bover = rbx;

    const reg64_t reg_tmp = rdx;
    const reg64_t reg_owb = rsi;
    const Xbyak::Opmask ktail_mask = Xbyak::Opmask(2);

    const Xbyak::Ymm ymm_tmp = Xbyak::Ymm(0);
    const Xbyak::Zmm zmm_tmp = Xbyak::Zmm(0);
    const Xbyak::Zmm zmm_zero = Xbyak::Zmm(1);

    void generate();
    void copy_row(int icb);
    void copy_row_body(int lpad, int iw_len, int icb);
};

struct jit_avx512_core_amx_fwd_kernel_t : public jit_generator {
    DECLARE_CPU_JIT_AUX_FUNCTIONS(jit_avx512_core_amx_fwd_kernel_t)

    jit_avx512_core_amx_fwd_kernel_t(
            jit_conv_conf_t ajcp, const primitive_attr_t &attr)
        : jcp(ajcp), attr_(attr), eltwise_injector_(nullptr) {
        if (jcp.with_eltwise)
            eltwise_injector_ = new jit_uni_eltwise_injector_f32<avx512_common>(
                    this, jcp.eltwise);
        full_tile_width_ = amx::get_max_rows(amx::get_max_palette());
        copy_to_pbuffer_ = new jit_avx512_core_amx_copy_to_pbuffer_t(jcp);
        tilecfg_ = new jit_avx512_core_amx_tilecfg_t(jcp);

        generate();

        jit_ker = (void (*)(jit_conv_call_s *))getCode();
        jit_copy_ker = (void (*)(jit_conv_call_s *))copy_to_pbuffer_->getCode();
        jit_tilecfg = (void (*)(void *))tilecfg_->getCode();
    }
    ~jit_avx512_core_amx_fwd_kernel_t() {
        delete eltwise_injector_;
        delete copy_to_pbuffer_;
        delete tilecfg_;
    }

    static bool post_ops_ok(jit_conv_conf_t &jcp, const primitive_attr_t &attr);

    static status_t init_conf(jit_conv_conf_t &jcp,
            const convolution_desc_t &cd, memory_desc_t &src_pd,
            memory_desc_t &weights_pd, memory_desc_t &dst_pd,
            memory_desc_t &bias_pd, const primitive_attr_t &attr, int nthreads);
    static void init_scratchpad(memory_tracking::registrar_t &scratchpad,
            const jit_conv_conf_t &jcp, const primitive_attr_t &attr);

    // Tile-registers decomposition and tile parameters
    enum { C_BASE = 0, W_BASE = 6, I_BASE = 4 };

    void tile_configure(char *tcfg_buff);

    jit_conv_conf_t jcp;
    const primitive_attr_t &attr_;
    void (*jit_ker)(jit_conv_call_s *);
    void (*jit_copy_ker)(jit_conv_call_s *);
    void (*jit_tilecfg)(void *);

private:
    jit_uni_eltwise_injector_f32<avx512_common> *eltwise_injector_;
    jit_avx512_core_amx_copy_to_pbuffer_t *copy_to_pbuffer_;
    jit_avx512_core_amx_tilecfg_t *tilecfg_;

    int prv_width_;
    int row_count_;
    bool is_store_done_;
    bool is_buffer_empty_;

    int full_tile_width_;

    /* data regs */
    const Xbyak::Reg64 inp_ptr = r15;
    const Xbyak::Reg64 wei_ptr = r14;
    const Xbyak::Reg64 out_ptr = r13;
    const Xbyak::Reg64 wsp_ptr = r12;

    const Xbyak::Reg64 reg_bias = r11;
    const Xbyak::Reg64 reg_ptr_scales = r10;
    const Xbyak::Reg64 reg_ptr_sum_scale = r9;
    const Xbyak::Reg64 aux_reg_saturation = reg_ptr_sum_scale;

    const Xbyak::Reg64 aux_inp_ptr = r8;
    const Xbyak::Reg64 aux_wei_ptr = rax;
    const Xbyak::Reg64 reg_inp_stride = rbx;
    const Xbyak::Reg64 reg_wei_stride = rdx;

    // rsi - free and available
    // rbp - reserved for EVEX compression
    const Xbyak::Reg64 reg_last_h = abi_not_param1;

    // temporary, used in generate() function only
    const Xbyak::Reg64 reg_oc_blocks = aux_wei_ptr;
    const Xbyak::Reg64 reg_tmp = aux_inp_ptr;

    const Xbyak::Opmask ktail_mask = Xbyak::Opmask(2);

    const Xbyak::Zmm zmm_bias = Xbyak::Zmm(31);
    const Xbyak::Zmm zmm_saturation = zmm_bias;
    const Xbyak::Zmm zmm_zero = Xbyak::Zmm(30);
    const Xbyak::Zmm zmm_prev_dst = Xbyak::Zmm(29);

    // AUX: Steps, shifts and offsets
    size_t get_inp_icb_step() const;
    size_t get_wei_icb_step() const;
    size_t get_inp_h_step() const;
    size_t get_wei_h_step() const;
    size_t get_out_ocb_offset(int ohb, int ocb) const;
    size_t get_out_row_offset(int ohb, int ocb, int j) const;
    size_t get_out_shift(int width) const;
    size_t get_wsp_ocb_offset(int ohb, int ocb) const;
    size_t get_wsp_row_offset(int ohb, int ocb, int j) const;
    size_t get_wsp_shift() const;
    size_t get_wei_offset(int ocb, int kw) const;
    size_t get_inp_shift() const;
    size_t get_inp_offset(int ohb, int kw) const;

    int get_out_tensor(int h, int i, int rem = false) const;
    int get_inp_tensor(int h, int rem = false) const;
    int get_wei_tensor(int i) const;

    void prepare_output(int tail);
    void init_runtime_counters(bool start_with_last_tile_block);

    bool maybe_eltwise(int position);
    void cvt2ps(data_type_t type_in, Xbyak::Zmm ymm_in,
            const Xbyak::Operand &op, bool mask_flag);
    const Xbyak::Ymm ymm_mask(
            const Xbyak::Ymm zmm_in, bool mask_flag, bool store = false);
    const Xbyak::Zmm zmm_mask(
            const Xbyak::Zmm zmm_in, bool mask_flag, bool store = false);

    void store_output_vector_bf16(
            const Xbyak::Zmm zmm_out, int ocb, int h, int w);
    void store_output_vector_int8(
            const Xbyak::Zmm zmm_out, int ocb, int h, int w);
    void store_output_vector(const Xbyak::Zmm zmm_out, int ocb, int h, int w);
    void store_output(int width, int tail, bool do_store);
    void interleave_store(int width);
    void compute_icb_loop(int width, bool do_store);
    void compute_ow_loop();

    void generate();
};

} // namespace x64
} // namespace cpu
} // namespace impl
} // namespace dnnl

#endif
