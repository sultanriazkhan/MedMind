import { toast } from 'sonner'
import { useCallback } from 'react'

export const useToast = () => {
  const showSuccess = useCallback((message, options = {}) => {
    toast.success(message, {
      position: 'top-right',
      duration: 4000,
      ...options
    })
  }, [])

  const showError = useCallback((message, options = {}) => {
    toast.error(message, {
      position: 'top-right',
      duration: 5000,
      ...options
    })
  }, [])

  const showInfo = useCallback((message, options = {}) => {
    toast.info(message, {
      position: 'top-right',
      duration: 3000,
      ...options
    })
  }, [])

  const showWarning = useCallback((message, options = {}) => {
    toast.warning(message, {
      position: 'top-right',
      duration: 4000,
      ...options
    })
  }, [])

  const showLoading = useCallback((message, options = {}) => {
    return toast.loading(message, {
      position: 'top-right',
      duration: Infinity,
      ...options
    })
  }, [])

  const dismiss = useCallback((toastId) => {
    toast.dismiss(toastId)
  }, [])

  const dismissAll = useCallback(() => {
    toast.dismiss()
  }, [])

  const showPromise = useCallback(async (promise, messages, options = {}) => {
    return toast.promise(promise, {
      loading: messages.loading || 'Processing...',
      success: messages.success || 'Success!',
      error: messages.error || 'Something went wrong',
      ...options
    })
  }, [])

  const showCustom = useCallback((message, options = {}) => {
    return toast.custom(message, {
      position: 'top-right',
      duration: 4000,
      ...options
    })
  }, [])

  const showApiError = useCallback((error, fallbackMessage = 'An error occurred') => {
    const message = error.response?.data?.error || error.message || fallbackMessage
    toast.error(message, {
      position: 'top-right',
      duration: 5000,
    })
  }, [])

  const showFormErrors = useCallback((errors) => {
    const firstError = Object.values(errors)[0]
    if (firstError) {
      toast.error(typeof firstError === 'string' ? firstError : firstError.message)
    }
  }, [])

  return {
    success: showSuccess,
    error: showError,
    info: showInfo,
    warning: showWarning,
    loading: showLoading,
    dismiss,
    dismissAll,
    promise: showPromise,
    custom: showCustom,
    apiError: showApiError,
    formErrors: showFormErrors
  }
}

export default useToast