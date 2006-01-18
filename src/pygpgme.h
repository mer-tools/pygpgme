/* -*- mode: C; c-basic-offset: 4; indent-tabs-mode: nil -*- */
#ifndef PYGPGME_H
#define PYGPGME_H

#include <Python.h>
#include <gpgme.h>

#define HIDDEN __attribute__((visibility("hidden")))

typedef struct {
    PyObject_HEAD
    gpgme_ctx_t ctx;
} PyGpgmeContext;

typedef struct {
    PyObject_HEAD
    gpgme_key_t key;
} PyGpgmeKey;

typedef struct {
    PyObject_HEAD
    gpgme_subkey_t subkey;
    PyObject *parent;
} PyGpgmeSubkey;

typedef struct {
    PyObject_HEAD
    gpgme_user_id_t user_id;
    PyObject *parent;
} PyGpgmeUserId;

typedef struct {
    PyObject_HEAD
    gpgme_key_sig_t key_sig;
    PyObject *parent;
} PyGpgmeKeySig;

typedef struct {
    PyObject_HEAD
    PyObject *type;
    PyObject *pubkey_algo;
    PyObject *hash_algo;
    PyObject *timestamp;
    PyObject *fpr;
    PyObject *sig_class;
} PyGpgmeNewSignature;

typedef struct {
    PyObject_HEAD
    PyObject *summary;
    PyObject *fpr;
    PyObject *status;
    PyObject *notations;
    PyObject *timestamp;
    PyObject *exp_timestamp;
    PyObject *wrong_key_usage;
    PyObject *validity;
    PyObject *validity_reason;
} PyGpgmeSignature;

typedef struct {
    PyObject_HEAD
    PyGpgmeContext *ctx;
} PyGpgmeKeyIter;

extern HIDDEN PyObject *pygpgme_error;
extern HIDDEN PyTypeObject PyGpgmeContext_Type;
extern HIDDEN PyTypeObject PyGpgmeKey_Type;
extern HIDDEN PyTypeObject PyGpgmeSubkey_Type;
extern HIDDEN PyTypeObject PyGpgmeUserId_Type;
extern HIDDEN PyTypeObject PyGpgmeKeySig_Type;
extern HIDDEN PyTypeObject PyGpgmeNewSignature_Type;
extern HIDDEN PyTypeObject PyGpgmeSignature_Type;
extern HIDDEN PyTypeObject PyGpgmeKeyIter_Type;

HIDDEN int           pygpgme_check_error    (gpgme_error_t err);
HIDDEN PyObject     *pygpgme_error_object   (gpgme_error_t err);
HIDDEN gpgme_error_t pygpgme_check_pyerror  (void);
HIDDEN int           pygpgme_no_constructor (PyObject *self, PyObject *args,
                                             PyObject *kwargs);

HIDDEN int           pygpgme_data_new       (gpgme_data_t *dh, PyObject *fp);
HIDDEN PyObject     *pygpgme_key_new        (gpgme_key_t key);
HIDDEN PyObject     *pygpgme_newsiglist_new (gpgme_new_signature_t siglist);
HIDDEN PyObject     *pygpgme_siglist_new    (gpgme_signature_t siglist);

#endif
