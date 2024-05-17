import React, { useState } from "react";
import {
  Nav,
  NavLink,
  Bars,
  NavMenu,
  NavBtn,
  NavBtnLink,
} from "./NavbarElements.js";

const Navbar = () => {
  return (
    <>
      <Nav>
        <Bars />

        <NavMenu>
          <NavLink to="/home">Home</NavLink>
          <NavLink to="/fileinput" activeStyle>
            Prediction
          </NavLink>
          <NavLink to="/playlist" activeStyle>
            Playlist
          </NavLink>
          {/* Second Nav */}
          {/* <NavBtnLink to='/sign-in'>Sign In</NavBtnLink> */}
        </NavMenu>
        {/*
                <NavBtn>
                    <NavBtnLink to="/login">
                        LogIn
                    </NavBtnLink>
                </NavBtn>
    */}
      </Nav>
    </>
  );
};

export default Navbar;
