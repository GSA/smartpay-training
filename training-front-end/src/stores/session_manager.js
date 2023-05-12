import { atom, onMount, action } from 'nanostores'
import { clearUser, hasActiveSession } from './user.js'
import { setMessage } from './message_manager.js'

const SESSION_TIME_OUT = import.meta.env.PUBLIC_SESSION_TIME_OUT * 60 * 1000
const SESSION_WARNING_TIME = import.meta.env.PUBLIC_SESSION_WARNING_TIME * 60 * 1000

// These window events will reset the timeout 
const LISTEN_EVENTS = ['mousedown', 'mousemove', 'scroll', 'keydown']

let warn_interval 
let session_timeout 

export const willTimeOut = atom(false)
export const didTimeOut = atom(false)

export const resetDidTimeOut = action(didTimeOut, 'resetDidTimeOut', store => store.set(false))
export const continueSession = action(willTimeOut, 'continueSession', prevent_session_end)

const setWindowListeners = () => LISTEN_EVENTS.forEach(
  event => window.addEventListener(event, reset_timeout)
)
const unSetWindowListeners = () => LISTEN_EVENTS.forEach(
  event => window.removeEventListener(event, reset_timeout)
)

export function exit() {
  clearUser()
  window.location.replace(import.meta.env.BASE_URL)
}

function set_warn_before_exit() {
  // Don't listen to window events once the warning is set
  // Once the warning is set it should need explicit action 
  // from user (like clicking modal button)
  unSetWindowListeners()
  willTimeOut.set(true)
}

function prevent_session_end() {
  // Explicitly reset timer. This should be the result of a user 
  // action like the click of a modal button
  setWindowListeners()
  reset_timeout()
}

function set_timeout() {
  warn_interval = setTimeout(set_warn_before_exit, SESSION_TIME_OUT - SESSION_WARNING_TIME)
  session_timeout  = setTimeout(() => {
    setMessage('Your session has timed out due to inactivity. Start a new session to take a training or access past certificates.')
    exit()
  }, SESSION_TIME_OUT)
}

function reset_timeout() {
  willTimeOut.set(false)
  clearTimeout(warn_interval)
  clearTimeout(session_timeout)
  set_timeout()
}

onMount(willTimeOut, () => {
  hasActiveSession.subscribe(active => {
    if (active) {
      setWindowListeners()
      set_timeout()
    } else {
      unSetWindowListeners()
    }  
  })
})
