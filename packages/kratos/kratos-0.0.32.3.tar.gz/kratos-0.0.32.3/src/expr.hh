#ifndef KRATOS_EXPR_HH
#define KRATOS_EXPR_HH

#include <optional>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

#include "context.hh"
#include "ir.hh"

namespace kratos {

enum class ExprOp : uint64_t {
    // unary
    UInvert,
    UMinus,
    UPlus,
    UOr,
    UNot,
    UAnd,
    UXor,

    // binary
    Add,
    Minus,
    Divide,
    Multiply,
    Mod,
    LogicalShiftRight,
    SignedShiftRight,
    ShiftLeft,
    Or,
    And,
    Xor,
    Power,
    // logical
    LAnd,
    LOr,

    // relational
    LessThan,
    GreaterThan,
    LessEqThan,
    GreaterEqThan,
    Eq,
    Neq,

    // ternary
    Conditional,

    // special
    Concat,
    Extend
};

bool is_relational_op(ExprOp op);
bool is_reduction_op(ExprOp op);
bool is_expand_op(ExprOp op);
bool is_unary_op(ExprOp op);
bool is_ternary_op(ExprOp op);

enum class VarType { Base, Expression, Slice, ConstValue, PortIO, Parameter, BaseCasted, Iter };

enum class VarCastType { Signed, Unsigned, Clock, AsyncReset, ClockEnable, Reset, Enum, Resize };

enum class ParamType { Integral, Parameter, Enum, RawType };

struct Var : public std::enable_shared_from_this<Var>, public IRNode {
public:
    Var(Generator *m, const std::string &name, uint32_t var_width, uint32_t size, bool is_signed);
    Var(Generator *m, const std::string &name, uint32_t var_width,
        const std::vector<uint32_t> &size, bool is_signed);
    Var(Generator *m, const std::string &name, uint32_t var_width, uint32_t size, bool is_signed,
        VarType type);
    Var(Generator *m, const std::string &name, uint32_t var_width, std::vector<uint32_t> size,
        bool is_signed, VarType type);

    std::string name;
    uint32_t &var_width() { return var_width_; }
    std::vector<uint32_t> &size() { return size_; }
    const std::vector<uint32_t> &size() const { return size_; }
    bool &is_signed() { return is_signed_; };
    virtual uint32_t width() const;
    uint32_t var_width() const { return var_width_; }
    bool is_signed() const { return is_signed_; };

    // overload all the operators
    // unary
    Expr &operator~() const;
    Expr &operator-() const;
    Expr &operator+() const;
    Expr &r_or() const;
    Expr &r_and() const;
    Expr &r_xor() const;
    Expr &r_not() const;
    // binary
    Expr &operator+(const Var &var) const;
    Expr &operator-(const Var &var) const;
    Expr &operator*(const Var &var) const;
    Expr &operator%(const Var &var) const;
    Expr &operator/(const Var &var) const;
    Expr &operator>>(const Var &var) const;
    Expr &operator<<(const Var &var) const;
    Expr &operator|(const Var &var) const;
    Expr &operator&(const Var &var) const;
    Expr &operator^(const Var &var) const;
    Expr &ashr(const Var &var) const;
    Expr &operator<(const Var &var) const;
    Expr &operator>(const Var &var) const;
    Expr &operator<=(const Var &var) const;
    Expr &operator>=(const Var &var) const;
    Expr &operator!=(const Var &var) const;
    Expr &eq(const Var &var) const;
    Expr &operator&&(const Var &var) const;
    Expr &operator||(const Var &var) const;
    // slice
    virtual VarSlice &operator[](std::pair<uint32_t, uint32_t> slice);
    virtual VarSlice &operator[](uint32_t bit);
    virtual VarSlice &operator[](const std::shared_ptr<Var> &var);
    // concat
    virtual VarConcat &concat(Var &var);
    // extend
    virtual VarExtend &extend(uint32_t width);
    // power
    Expr &pow(const Var &var) const;

    std::shared_ptr<Var> cast(VarCastType cast_type);

    // assignment
    std::shared_ptr<AssignStmt> assign(const std::shared_ptr<Var> &var);
    std::shared_ptr<AssignStmt> assign(Var &var);
    std::shared_ptr<AssignStmt> assign(const std::shared_ptr<Var> &var, AssignmentType type);
    std::shared_ptr<AssignStmt> assign(Var &var, AssignmentType type);
    void unassign(const std::shared_ptr<AssignStmt> &stmt);

    virtual Generator *generator() const { return generator_; }
    void set_generator(Generator *gen) { generator_ = gen; }

    IRNode *parent() override;

    VarType type() const { return type_; }
    virtual const std::unordered_set<std::shared_ptr<AssignStmt>> &sinks() const { return sinks_; };
    virtual void remove_sink(const std::shared_ptr<AssignStmt> &stmt) { sinks_.erase(stmt); }
    virtual const std::unordered_set<std::shared_ptr<AssignStmt>> &sources() const {
        return sources_;
    };
    virtual void clear_sinks(bool remove_parent);
    virtual void clear_sources(bool remove_parent);
    virtual void remove_source(const std::shared_ptr<AssignStmt> &stmt) { sources_.erase(stmt); }
    std::vector<std::shared_ptr<VarSlice>> &get_slices() { return slices_; }

    static void move_src_to(Var *var, Var *new_var, Generator *parent, bool keep_connection);
    static void move_sink_to(Var *var, Var *new_var, Generator *parent, bool keep_connection);
    virtual void move_linked_to(Var *new_var);
    virtual void add_sink(const std::shared_ptr<AssignStmt> &stmt) { sinks_.emplace(stmt); }
    virtual void add_source(const std::shared_ptr<AssignStmt> &stmt) { sources_.emplace(stmt); }
    void add_concat_var(const std::shared_ptr<VarConcat> &var) { concat_vars_.emplace(var); }

    template <typename T>
    std::shared_ptr<T> as() {
        return std::static_pointer_cast<T>(shared_from_this());
    }

    virtual bool inline is_struct() const { return false; }
    virtual bool inline is_packed() const { return is_packed_; }
    virtual void set_is_packed(bool value) { is_packed_ = value; }
    virtual bool inline is_enum() const { return false; }
    virtual bool inline is_param() const { return false; }
    virtual bool inline is_function() const { return false; }
    virtual bool inline is_interface() const { return false; }
    virtual std::shared_ptr<Var> slice_var(std::shared_ptr<Var> var) { return var; }

    virtual std::string to_string() const;

    // AST stuff
    void accept(IRVisitor *visitor) override { visitor->visit(this); }
    uint64_t child_count() override;
    IRNode *get_child(uint64_t) override;

    // meta info
    // packed is only relevant when the size is larger than 1, by default it's false
    virtual std::string handle_name() const;
    virtual std::string handle_name(bool ignore_top) const;
    virtual std::string handle_name(Generator *scope) const;
    // is parametrized
    bool parametrized() const { return width_param_ != nullptr; }
    void set_width_param(const std::shared_ptr<Var> &param);
    void set_width_param(Var *param);
    Var *width_param() const { return width_param_; }
    bool raw_type_parametrized() const { return raw_type_param_ != nullptr; }
    void set_raw_type_param(Param *param) { raw_type_param_ = param; }
    Param *get_raw_type_param() { return raw_type_param_; }
    void set_explicit_array(bool value) { explicit_array_ = value; }
    bool explicit_array() const { return explicit_array_; }
    virtual std::vector<std::pair<uint32_t, uint32_t>> get_slice_index() const { return {}; }
    virtual uint32_t var_high() const { return width() - 1; }
    virtual uint32_t var_low() const { return 0; }

    [[nodiscard]] virtual std::string base_name() const { return name; }

    // for slice
    virtual const Var *get_var_root_parent() const { return this; }
    virtual Var *get_var_root_parent() { return this; }

    // before and after strings. they're used for downstream tools. kratos doesn't care about the
    // value. it's user's responsibility to make it legal syntax
    inline void set_before_var_str_(const std::string &value) { before_var_str_ = value; }
    inline const std::string &before_var_str() const { return before_var_str_; }
    inline void set_after_var_str_(const std::string &value) { after_var_str_ = value; }
    inline const std::string &after_var_str() const { return after_var_str_; }

    // assign a particular parameter to parametrize the size at given dimension
    // will do a sanity check to make sure that the changed size won't affect already existing
    // slices
    void set_size_param(uint32_t index, Var *param);
    inline Var *get_size_param(uint32_t index) const {
        return size_param_.find(index) == size_param_.end() ? nullptr : size_param_.at(index);
    }

    // copy metadata over
    void copy_meta_data(Var *new_var, bool check_param) const;

    Var(const Var &var) = delete;
    Var() = delete;

    ~Var() override = default;

protected:
    uint32_t var_width_;
    std::vector<uint32_t> size_;
    std::unordered_map<uint32_t, Var *> size_param_;
    bool is_signed_;

    std::unordered_set<std::shared_ptr<AssignStmt>> sinks_;
    std::unordered_set<std::shared_ptr<AssignStmt>> sources_;

    VarType type_ = VarType::Base;

    std::unordered_set<std::shared_ptr<VarConcat>> concat_vars_;

    std::vector<std::shared_ptr<VarSlice>> slices_;

    // comment values
    std::string before_var_str_;
    std::string after_var_str_;

    // special values
    bool explicit_array_ = false;

    // parametrization
    Var *width_param_ = nullptr;
    // raw type parametrization
    Param *raw_type_param_ = nullptr;

    bool is_packed_ = false;

    Generator *generator_;

    // assign function
    virtual std::shared_ptr<AssignStmt> assign_(const std::shared_ptr<Var> &var,
                                                AssignmentType type);


private:
    std::set<std::shared_ptr<VarCasted>> casted_;
    std::unordered_map<uint32_t, std::shared_ptr<VarExtend>> extended_;
};

struct EnumType {
public:
    [[nodiscard]] virtual const Enum *enum_type() const = 0;
};

struct VarCasted : public Var, public EnumType {
public:
    VarCasted(Var *parent, VarCastType cast_type);

    Generator *generator() const override { return parent_var_->generator(); }

    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override;
    void set_parent(Var *parent) { parent_var_ = parent; }

    const Var *get_var_root_parent() const override { return parent_var_->get_var_root_parent(); }
    Var *get_var_root_parent() override { return parent_var_->get_var_root_parent(); }

    Var *&parent_var() { return parent_var_; }

    std::string to_string() const override;

    VarCastType cast_type() const { return cast_type_; }

    // wraps all the critical functions
    // ideally this should be in another sub-class of Var and modport version as well
    // however, getting this to work with pybind with virtual inheritance is a pain
    // so just copy the code here
    const std::unordered_set<std::shared_ptr<AssignStmt>> &sinks() const override {
        return parent_var_->sinks();
    };
    void remove_sink(const std::shared_ptr<AssignStmt> &stmt) override {
        parent_var_->remove_sink(stmt);
    }
    const std::unordered_set<std::shared_ptr<AssignStmt>> &sources() const override {
        return parent_var_->sources();
    };
    void clear_sinks(bool remove_parent) override { parent_var_->clear_sources(remove_parent); }
    void clear_sources(bool remove_parent) override { parent_var_->clear_sinks(remove_parent); }
    void remove_source(const std::shared_ptr<AssignStmt> &stmt) override {
        parent_var_->remove_source(stmt);
    }

    void move_linked_to(Var *new_var) override { parent_var_->move_linked_to(new_var); }

    void set_enum_type(Enum *enum_) { enum_type_ = enum_; }
    const Enum *enum_type() const override { return enum_type_; }

    bool is_enum() const override { return cast_type_ == VarCastType ::Enum; }

    void set_target_width(uint32_t width);

protected:
    std::shared_ptr<AssignStmt> assign_(const std::shared_ptr<Var> &var,
                                        AssignmentType type) override;

private:
    Var *parent_var_ = nullptr;

    VarCastType cast_type_;
    // only used for enum
    Enum *enum_type_ = nullptr;
    // only used for resize
    uint32_t target_width_ = 0;
};

struct VarSlice : public Var {
public:
    Var *parent_var = nullptr;
    uint32_t low = 0;
    uint32_t high = 0;

    VarSlice(Var *parent, uint32_t high, uint32_t low);
    IRNode *parent() override;

    // we tie it to the parent
    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override;
    void add_source(const std::shared_ptr<AssignStmt> &stmt) override;
    void remove_source(const std::shared_ptr<AssignStmt> &stmt) override;
    void remove_sink(const std::shared_ptr<AssignStmt> &stmt) override;

    void set_parent(Var *parent) { parent_var = parent; }

    void accept(IRVisitor *visitor) override { visitor->visit(this); }

    std::string to_string() const override;

    uint32_t var_high() const override { return var_high_; }
    uint32_t var_low() const override { return var_low_; }

    std::shared_ptr<Var> slice_var(std::shared_ptr<Var> var) override {
        return var->operator[](op_).shared_from_this();
    }

    std::vector<std::pair<uint32_t, uint32_t>> get_slice_index() const override;

    PackedSlice &operator[](const std::string &member_name);
    VarSlice &operator[](uint32_t index) override { return Var::operator[](index); }
    VarSlice &operator[](std::pair<uint32_t, uint32_t> slice) override {
        return Var::operator[](slice);
    }
    VarSlice &operator[](const std::shared_ptr<Var> &slice) override {
        return Var::operator[](slice);
    }

    const Var *get_var_root_parent() const override;
    Var *get_var_root_parent() override;

    virtual bool sliced_by_var() const { return false; }

protected:
    uint32_t var_high_ = 0;
    uint32_t var_low_ = 0;

    std::pair<uint32_t, uint32_t> op_;
};

struct VarVarSlice : public VarSlice {
    // the name is a little bit funny
public:
    VarVarSlice(Var *parent, Var *slice);

    std::string to_string() const override;

    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override;
    void add_source(const std::shared_ptr<AssignStmt> &stmt) override;
    void remove_source(const std::shared_ptr<AssignStmt> &stmt) override;
    void remove_sink(const std::shared_ptr<AssignStmt> &stmt) override;

    std::shared_ptr<Var> slice_var(std::shared_ptr<Var> var) override {
        return var->operator[](sliced_var_->shared_from_this()).shared_from_this();
    }

    bool sliced_by_var() const override { return true; }
    Var *sliced_var() const { return sliced_var_; }

    void accept(IRVisitor *visitor) override { visitor->visit(this); }

private:
    Var *sliced_var_;
};

struct Const : public Var {
    // need to rewrite the const backend since the biggest number is uint64_t, which may not
public:
    Const(Generator *m, int64_t value, uint32_t width, bool is_signed);

    int64_t value() const { return value_; }
    virtual void set_value(int64_t new_value);
    void add_source(const std::shared_ptr<AssignStmt> &stmt) override;
    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override;
    void set_width(uint32_t target_width);

    std::string to_string() const override;
    std::string handle_name(bool) const override { return to_string(); }
    std::string handle_name(Generator *) const override { return to_string(); }

    void accept(IRVisitor *visitor) override { visitor->visit(this); }

    static Const &constant(int64_t value, uint32_t width, bool is_signed);
    Const(int64_t value, uint32_t width, bool is_signed);

    static Generator *const_gen() { return const_generator_.get(); }

    // struct is always packed
    bool is_packed() const override { return true; }
    void set_is_packed(bool value) override;

    enum class ConstantLegal { Legal, Small, Big };

    static ConstantLegal is_legal(int64_t value, uint32_t width, bool is_signed);

private:
    int64_t value_;
    // created without a generator holder
    static std::unordered_set<std::shared_ptr<Const>> consts_;
    static std::shared_ptr<Generator> const_generator_;
};

// helper function
inline Const &constant(int64_t value, uint32_t width, bool is_signed = false) {
    return Const::constant(value, width, is_signed);
}

struct Param : public Const {
public:
    Param(Generator *m, std::string name, uint32_t width, bool is_signed);
    // raw type. only used for interacting with imported modules
    Param(Generator *m, std::string name);
    Param(Generator *m, std::string name, Enum *enum_def);
    Param(Generator *m, const std::shared_ptr<Param> &param, std::string parameter_name);

    void accept(IRVisitor *visitor) override { visitor->visit(this); }

    std::string inline to_string() const override { return parameter_name_; }

    std::string value_str() const;
    inline bool has_value() const { return has_value_; }

    void add_param_width_var(Var *var) { param_vars_width_.emplace(var); }
    void add_param_size_var(Var *var, uint32_t index, Var *expr);

    void set_value(int64_t new_value) override;
    void set_value(const std::shared_ptr<Param> &param);
    // used as raw string
    void set_value(const std::string &str_value);
    void set_initial_value(int64_t new_value) { initial_value_ = new_value; }
    std::optional<int64_t> get_initial_value() const { return initial_value_; }
    std::optional<std::string> get_raw_str_value() const { return raw_str_value_; }
    void set_initial_raw_str_value(const std::string &value) { initial_raw_str_value_ = value; }
    std::optional<std::string> get_raw_str_initial_value() const { return initial_raw_str_value_; }

    bool is_param() const override { return true; }

    const Param *parent_param() const { return parent_param_; }
    ParamType param_type() const { return param_type_; }
    Enum *enum_def() const { return enum_def_; }

    [[nodiscard]] const std::string &parameter_name() const { return parameter_name_; }

private:
    std::string parameter_name_;
    ParamType param_type_ = ParamType::Integral;

    std::unordered_set<Var *> param_vars_width_;
    std::set<std::tuple<Var *, uint32_t, Var *>> param_vars_size_;
    std::unordered_set<Param *> param_params_;
    Param *parent_param_ = nullptr;

    bool has_value_ = false;
    std::optional<int64_t> initial_value_;
    // for now only used for raw_type strings
    std::optional<std::string> raw_str_value_;
    std::optional<std::string> initial_raw_str_value_;
    Enum *enum_def_ = nullptr;
};

struct PackedStruct {
public:
    std::string struct_name;
    std::vector<std::tuple<std::string, uint32_t, bool>> attributes;
    bool external = false;

    PackedStruct(std::string struct_name,
                 std::vector<std::tuple<std::string, uint32_t, bool>> attributes);
    PackedStruct(std::string struct_name,
                 const std::vector<std::tuple<std::string, uint32_t>> &attributes);
};

struct PackedSlice : public VarSlice {
public:
    PackedSlice(PortPackedStruct *parent, const std::string &member_name);
    PackedSlice(VarPackedStruct *parent, const std::string &member_name);

    // this is used for packed struct array
    PackedSlice(VarSlice *slice, bool is_root);

    PackedSlice &slice_member(const std::string &member_name);

    std::string to_string() const override;

    std::shared_ptr<Var> slice_var(std::shared_ptr<Var> var) override;

private:
    void set_up(const PackedStruct &struct_, const std::string &member_name);
    std::string member_name_;

    bool is_root_ = false;
};

struct PackedInterface {
    [[nodiscard]] virtual std::set<std::string> member_names() const = 0;
    virtual ~PackedInterface() = default;
};

struct VarPackedStruct : public Var, public PackedInterface {
public:
    VarPackedStruct(Generator *m, const std::string &name, PackedStruct packed_struct_);
    VarPackedStruct(Generator *m, const std::string &name, PackedStruct packed_struct_,
                    uint32_t size);
    VarPackedStruct(Generator *m, const std::string &name, PackedStruct packed_struct_,
                    const std::vector<uint32_t> &size);

    bool is_struct() const override { return true; }

    const PackedStruct &packed_struct() const { return struct_; }

    PackedSlice &operator[](const std::string &member_name);

    // necessary to make pybind happy due to complex inheritance
    VarSlice inline &operator[](std::pair<uint32_t, uint32_t> slice) override {
        return Var::operator[](slice);
    }
    VarSlice inline &operator[](uint32_t idx) override { return Var::operator[](idx); }

    std::set<std::string> member_names() const override;

    // struct is always packed
    bool is_packed() const override { return true; }
    void set_is_packed(bool value) override;

private:
    PackedStruct struct_;

    void compute_width();
};

struct Expr : public Var {
public:
    ExprOp op;
    Var *left;
    Var *right;

    Expr(ExprOp op, Var *left, Var *right);
    std::string to_string() const override;
    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override;

    uint32_t width() const override;

    // AST
    void accept(IRVisitor *visitor) override { visitor->visit(this); }
    uint64_t child_count() override { return right ? 2 : 1; }
    IRNode *get_child(uint64_t index) override;

    std::string handle_name(bool ignore_top) const override;
    std::string handle_name(Generator *scope) const override;

protected:
    // caller is responsible for the op
    Expr(Var *left, Var *right);

private:
    void set_parent();
};

struct VarConcat : public Expr {
public:
    VarConcat(const std::shared_ptr<Var> &first, const std::shared_ptr<Var> &second);
    VarConcat(const std::shared_ptr<VarConcat> &first, const std::shared_ptr<Var> &second);

    // we tie it to the parent
    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override;
    void add_source(const std::shared_ptr<AssignStmt> &stmt) override;

    const std::vector<Var *> &vars() const { return vars_; }
    void replace_var(const std::shared_ptr<Var> &target, const std::shared_ptr<Var> &item);

    VarConcat &concat(Var &var) override;

    uint64_t child_count() override { return vars_.size(); }
    IRNode *get_child(uint64_t index) override {
        return index < vars_.size() ? vars_[index] : nullptr;
    }

    uint32_t width() const override { return var_width_; }

    void accept(IRVisitor *visitor) override { visitor->visit(this); }

    std::string to_string() const override;
    std::string handle_name(bool ignore_top) const override;
    std::string handle_name(Generator *scope) const override;

private:
    std::vector<Var *> vars_;
};

struct VarExtend : public Expr {
public:
    VarExtend(const std::shared_ptr<Var> &var, uint32_t width);

    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override;
    void add_source(const std::shared_ptr<AssignStmt> &stmt) override;
    void replace_var(const std::shared_ptr<Var> &target, const std::shared_ptr<Var> &item);

    uint32_t width() const override { return var_width_; }

    uint64_t child_count() override { return 1; }
    IRNode *get_child(uint64_t index) override { return index == 0 ? parent_ : nullptr; }

    std::string to_string() const override;
    Var *parent_var() const { return parent_; }

private:
    Var *parent_;
};

struct ConditionalExpr : public Expr {
    ConditionalExpr(const std::shared_ptr<Var> &condition, const std::shared_ptr<Var> &left,
                    const std::shared_ptr<Var> &right);
    uint64_t child_count() override { return 3; }
    IRNode *get_child(uint64_t index) override;
    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override;
    std::string to_string() const override;
    std::string handle_name(bool ignore_top) const override;
    std::string handle_name(Generator *scope) const override;

    Var *condition;
};

struct EnumConst : public Const {
public:
    EnumConst(Generator *m, int64_t value, uint32_t width, Enum *parent, std::string name);
    std::string to_string() const override;
    std::string value_string() { return Const::to_string(); }

    bool inline is_enum() const override { return true; }
    const inline Enum *enum_def() const { return parent_; }

    void accept(IRVisitor *visitor) override { visitor->visit(this); }

private:
    Enum *parent_;
    std::string name_;
};

struct Enum : std::enable_shared_from_this<Enum> {
public:
    Enum(const std::string &name, const std::map<std::string, uint64_t> &values, uint32_t width);
    std::map<std::string, std::shared_ptr<EnumConst>> values;
    std::string name;
    bool external = false;

    uint32_t inline width() const { return width_; }

    std::shared_ptr<EnumConst> get_enum(const std::string &name);
    void add_debug_info(const std::string &enum_name,
                        const std::pair<std::string, uint32_t> &debug);

    static void verify_naming_conflict(const std::map<std::string, std::shared_ptr<Enum>> &enums,
                                       const std::string &name,
                                       const std::map<std::string, uint64_t> &values);

    bool local() const { return local_; }
    bool &local() { return local_; }

private:
    uint32_t width_;
    bool local_ = true;
};

struct EnumVar : public Var, public EnumType {
public:
    bool inline is_enum() const override { return true; }

    EnumVar(Generator *m, const std::string &name, const std::shared_ptr<Enum> &enum_type)
        : Var(m, name, enum_type->width(), 1, false), enum_type_(enum_type.get()) {}

    const inline Enum *enum_type() const override { return enum_type_; }
    void accept(IRVisitor *visitor) override { visitor->visit(this); }

protected:
    std::shared_ptr<AssignStmt> assign_(const std::shared_ptr<Var> &var,
                                        AssignmentType type) override;

private:
    Enum *enum_type_;
};

struct FunctionCallVar : public Var {
public:
    FunctionCallVar(Generator *m, const std::shared_ptr<FunctionStmtBlock> &func_def,
                    const std::map<std::string, std::shared_ptr<Var>> &args,
                    bool has_return = true);
    bool is_function() const override { return true; }
    FunctionStmtBlock *func() const { return func_def_; }

    VarSlice &operator[](std::pair<uint32_t, uint32_t>) override {
        throw std::runtime_error("Slice a function call is not allowed");
    };
    VarSlice &operator[](uint32_t) override {
        throw std::runtime_error("Slice a function call is not allowed");
    };

    std::string to_string() const override;

    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override;
    void add_source(const std::shared_ptr<AssignStmt> &) override {
        throw std::runtime_error("Slice a function call is not allowed");
    }

    void accept(IRVisitor *visitor) override { visitor->visit(this); }

    const std::map<std::string, std::shared_ptr<Var>> &args() const { return args_; }

private:
    FunctionStmtBlock *func_def_;
    std::map<std::string, std::shared_ptr<Var>> args_;
};

struct InterfaceVar : public Var {
public:
    InterfaceVar(InterfaceRef *interface, Generator *m, const std::string &name, uint32_t var_width,
                 const std::vector<uint32_t> &size, bool is_signed)
        : Var(m, name, var_width, size, is_signed), interface_(interface) {}

    std::string to_string() const override;

    bool inline is_interface() const override { return true; }

    std::string base_name() const override;

private:
    InterfaceRef *interface_ = nullptr;
};

class IterVar : public Var {
public:
    IterVar(Generator *m, const std::string &name, int64_t min_value, int64_t max_value,
            bool signed_ = false);

    bool static safe_to_resize(const Var *var, uint32_t target_size, bool is_signed);
    static bool has_iter_var(const Var *var);
    static void fix_width(Var *&var, uint32_t target_width);

    [[nodiscard]] inline int64_t min_value() const { return min_value_; }
    [[nodiscard]] inline int64_t max_value() const { return max_value_; }

private:
    int64_t min_value_;
    int64_t max_value_;
};

// helper functions
namespace util {
std::shared_ptr<Expr> mux(Var &cond, Var &left, Var &right);
}

}  // namespace kratos
#endif  // KRATOS_EXPR_HH
