difference(){
   difference(){
      difference(){
         difference(){
            difference(){
               difference(){
                  difference(){
                     union(){
                        translate( [ 1.000000, 1.000000, 1.000000 ] ){
                           union(){
                              translate( [ 0.000000, 0.000000, 0.000000 ] ){
                                 sphere( r=1.000000, $fn=32 );
                              }translate( [ 33.000000, 0.000000, 0.000000 ] ){
                                 sphere( r=1.000000, $fn=32 );
                              }translate( [ 0.000000, 33.000000, 0.000000 ] ){
                                 sphere( r=1.000000, $fn=32 );
                              }translate( [ 33.000000, 33.000000, 0.000000 ] ){
                                 sphere( r=1.000000, $fn=32 );
                              }translate( [ 0.000000, 0.000000, 33.000000 ] ){
                                 sphere( r=1.000000, $fn=32 );
                              }translate( [ 33.000000, 0.000000, 33.000000 ] ){
                                 sphere( r=1.000000, $fn=32 );
                              }translate( [ 0.000000, 33.000000, 33.000000 ] ){
                                 sphere( r=1.000000, $fn=32 );
                              }translate( [ 33.000000, 33.000000, 33.000000 ] ){
                                 sphere( r=1.000000, $fn=32 );
                              }
                           }
                        }translate( [ 0.000000, 0.000000, 1.000000 ] ){
                           linear_extrude( height=33.000000, twist=0.000000, scale=1.000000, $fn=32 )
                           {
                              union(){
                                 translate( [ 1.000000, 1.000000 ] ){
                                    union(){
                                       translate( [ 0.000000, 0.000000 ] ){
                                          circle( r=1.000000, $fn=32 );
                                       }translate( [ 33.000000, 0.000000 ] ){
                                          circle( r=1.000000, $fn=32 );
                                       }translate( [ 0.000000, 33.000000 ] ){
                                          circle( r=1.000000, $fn=32 );
                                       }translate( [ 33.000000, 33.000000 ] ){
                                          circle( r=1.000000, $fn=32 );
                                       }
                                    }
                                 }translate( [ 0.000000, 1.000000 ] ){
                                    square( [ 35.000000, 33.000000 ] );
                                 }translate( [ 1.000000, 0.000000 ] ){
                                    square( [ 33.000000, 35.000000 ] );
                                 }
                              }
                           }
                        }translate( [ 0.000000, 34.000000, 0.000000 ] ){
                           rotate( [ 90.000000, 0.000000, 0.000000 ] ){
                              linear_extrude( height=33.000000, twist=0.000000, scale=1.000000, $fn=32 )
                              {
                                 union(){
                                    translate( [ 1.000000, 1.000000 ] ){
                                       union(){
                                          translate( [ 0.000000, 0.000000 ] ){
                                             circle( r=1.000000, $fn=32 );
                                          }translate( [ 33.000000, 0.000000 ] ){
                                             circle( r=1.000000, $fn=32 );
                                          }translate( [ 0.000000, 33.000000 ] ){
                                             circle( r=1.000000, $fn=32 );
                                          }translate( [ 33.000000, 33.000000 ] ){
                                             circle( r=1.000000, $fn=32 );
                                          }
                                       }
                                    }translate( [ 0.000000, 1.000000 ] ){
                                       square( [ 35.000000, 33.000000 ] );
                                    }translate( [ 1.000000, 0.000000 ] ){
                                       square( [ 33.000000, 35.000000 ] );
                                    }
                                 }
                              }
                           }
                        }translate( [ 34.000000, 0.000000, 0.000000 ] ){
                           rotate( [ 0.000000, -90.000000, 0.000000 ] ){
                              linear_extrude( height=33.000000, twist=0.000000, scale=1.000000, $fn=32 )
                              {
                                 union(){
                                    translate( [ 1.000000, 1.000000 ] ){
                                       union(){
                                          translate( [ 0.000000, 0.000000 ] ){
                                             circle( r=1.000000, $fn=32 );
                                          }translate( [ 33.000000, 0.000000 ] ){
                                             circle( r=1.000000, $fn=32 );
                                          }translate( [ 0.000000, 33.000000 ] ){
                                             circle( r=1.000000, $fn=32 );
                                          }translate( [ 33.000000, 33.000000 ] ){
                                             circle( r=1.000000, $fn=32 );
                                          }
                                       }
                                    }translate( [ 0.000000, 1.000000 ] ){
                                       square( [ 35.000000, 33.000000 ] );
                                    }translate( [ 1.000000, 0.000000 ] ){
                                       square( [ 33.000000, 35.000000 ] );
                                    }
                                 }
                              }
                           }
                        }
                     }
                     translate( [ 32.000000, 3.000000, 0.000000 ] ){
                        mirror( [ 1.000000, 0.000000, 0.000000 ] ){
                           linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
                           {
                              union(){
                                 difference(){
                                    square( [ 29.000000, 29.000000 ] );
                                    translate( [ 1.000000, 1.000000 ] ){
                                       square( [ 27.000000, 27.000000 ] );
                                    }
                                 }translate( [ 3.000000, 3.000000 ] ){
                                    resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                                       text( "TI", 10.000000, $fn=32  );
                                    }
                                 }
                              }
                           }
                        }
                     }
                  }
                  translate( [ 32.000000, 34.000000, 3.000000 ] ){
                     rotate( [ 90.000000, 0.000000, 180.000000 ] ){
                        linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
                        {
                           union(){
                              difference(){
                                 square( [ 29.000000, 29.000000 ] );
                                 translate( [ 1.000000, 1.000000 ] ){
                                    square( [ 27.000000, 27.000000 ] );
                                 }
                              }translate( [ 3.000000, 3.000000 ] ){
                                 resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                                    text( "AI", 10.000000, $fn=32  );
                                 }
                              }
                           }
                        }
                     }
                  }
               }
               translate( [ 34.000000, 3.000000, 32.000000 ] ){
                  rotate( [ 0.000000, 90.000000, 0.000000 ] ){
                     linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
                     {
                        union(){
                           difference(){
                              square( [ 29.000000, 29.000000 ] );
                              translate( [ 1.000000, 1.000000 ] ){
                                 square( [ 27.000000, 27.000000 ] );
                              }
                           }translate( [ 3.000000, 3.000000 ] ){
                              resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                                 text( "BIM", 10.000000, $fn=32  );
                              }
                           }
                        }
                     }
                  }
               }
            }
            translate( [ 1.000000, 3.000000, 3.000000 ] ){
               rotate( [ 0.000000, -90.000000, 0.000000 ] ){
                  linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
                  {
                     union(){
                        difference(){
                           square( [ 29.000000, 29.000000 ] );
                           translate( [ 1.000000, 1.000000 ] ){
                              square( [ 27.000000, 27.000000 ] );
                           }
                        }translate( [ 3.000000, 3.000000 ] ){
                           union(){
                              translate( [ 0.000000, 13.500000, 0.000000 ] ){
                                 resize( [ 23.000000, 9.500000 ], auto=[false, false, true] ){
                                    text( "Open", 10.000000, $fn=32  );
                                 }
                              }resize( [ 23.000000, 9.500000 ], auto=[false, false, true] ){
                                 text( "ICT", 10.000000, $fn=32  );
                              }
                           }
                        }
                     }
                  }
               }
            }
         }
         translate( [ 3.000000, 1.000000, 3.000000 ] ){
            rotate( [ 90.000000, 0.000000, 0.000000 ] ){
               linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
               {
                  union(){
                     difference(){
                        square( [ 29.000000, 29.000000 ] );
                        translate( [ 1.000000, 1.000000 ] ){
                           square( [ 27.000000, 27.000000 ] );
                        }
                     }translate( [ 3.000000, 3.000000 ] ){
                        resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                           text( "SD", 10.000000, $fn=32  );
                        }
                     }
                  }
               }
            }
         }
      }
      translate( [ 3.000000, 3.000000, 34.000000 ] ){
         linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
         {
            union(){
               difference(){
                  square( [ 29.000000, 29.000000 ] );
                  translate( [ 1.000000, 1.000000 ] ){
                     square( [ 27.000000, 27.000000 ] );
                  }
               }translate( [ 3.000000, 3.000000 ] ){
                  resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                     text( "CSC", 10.000000, $fn=32  );
                  }
               }
            }
         }
      }
   }
   union(){
      union(){
         union(){
            union(){
               union(){
                  union(){
                     union(){
                        translate( [ 1.000000, 1.000000, 1.000000 ] ){
                           union(){
                              translate( [ 0.000000, 0.000000, 0.000000 ] ){
                              }translate( [ 33.000000, 0.000000, 0.000000 ] ){
                              }translate( [ 0.000000, 33.000000, 0.000000 ] ){
                              }translate( [ 33.000000, 33.000000, 0.000000 ] ){
                              }translate( [ 0.000000, 0.000000, 33.000000 ] ){
                              }translate( [ 33.000000, 0.000000, 33.000000 ] ){
                              }translate( [ 0.000000, 33.000000, 33.000000 ] ){
                              }translate( [ 33.000000, 33.000000, 33.000000 ] ){
                              }
                           }
                        }translate( [ 0.000000, 0.000000, 1.000000 ] ){
                           linear_extrude( height=33.000000, twist=0.000000, scale=1.000000, $fn=32 )
                           {
                              union(){
                                 translate( [ 1.000000, 1.000000 ] ){
                                    union(){
                                       translate( [ 0.000000, 0.000000 ] ){
                                       }translate( [ 33.000000, 0.000000 ] ){
                                       }translate( [ 0.000000, 33.000000 ] ){
                                       }translate( [ 33.000000, 33.000000 ] ){
                                       }
                                    }
                                 }translate( [ 0.000000, 1.000000 ] ){
                                 }translate( [ 1.000000, 0.000000 ] ){
                                 }
                              }
                           }
                        }translate( [ 0.000000, 34.000000, 0.000000 ] ){
                           rotate( [ 90.000000, 0.000000, 0.000000 ] ){
                              linear_extrude( height=33.000000, twist=0.000000, scale=1.000000, $fn=32 )
                              {
                                 union(){
                                    translate( [ 1.000000, 1.000000 ] ){
                                       union(){
                                          translate( [ 0.000000, 0.000000 ] ){
                                          }translate( [ 33.000000, 0.000000 ] ){
                                          }translate( [ 0.000000, 33.000000 ] ){
                                          }translate( [ 33.000000, 33.000000 ] ){
                                          }
                                       }
                                    }translate( [ 0.000000, 1.000000 ] ){
                                    }translate( [ 1.000000, 0.000000 ] ){
                                    }
                                 }
                              }
                           }
                        }translate( [ 34.000000, 0.000000, 0.000000 ] ){
                           rotate( [ 0.000000, -90.000000, 0.000000 ] ){
                              linear_extrude( height=33.000000, twist=0.000000, scale=1.000000, $fn=32 )
                              {
                                 union(){
                                    translate( [ 1.000000, 1.000000 ] ){
                                       union(){
                                          translate( [ 0.000000, 0.000000 ] ){
                                          }translate( [ 33.000000, 0.000000 ] ){
                                          }translate( [ 0.000000, 33.000000 ] ){
                                          }translate( [ 33.000000, 33.000000 ] ){
                                          }
                                       }
                                    }translate( [ 0.000000, 1.000000 ] ){
                                    }translate( [ 1.000000, 0.000000 ] ){
                                    }
                                 }
                              }
                           }
                        }
                     }
                     translate( [ 32.000000, 3.000000, 0.000000 ] ){
                        mirror( [ 1.000000, 0.000000, 0.000000 ] ){
                           linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
                           {
                              union(){
                                 union(){
                                    translate( [ 1.000000, 1.000000 ] ){
                                    }
                                 }translate( [ 3.000000, 3.000000 ] ){
                                    resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                                    }
                                 }
                              }
                           }
                        }
                     }
                  }
                  translate( [ 32.000000, 34.000000, 3.000000 ] ){
                     rotate( [ 90.000000, 0.000000, 180.000000 ] ){
                        linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
                        {
                           union(){
                              union(){
                                 translate( [ 1.000000, 1.000000 ] ){
                                 }
                              }translate( [ 3.000000, 3.000000 ] ){
                                 resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                                 }
                              }
                           }
                        }
                     }
                  }
               }
               translate( [ 34.000000, 3.000000, 32.000000 ] ){
                  rotate( [ 0.000000, 90.000000, 0.000000 ] ){
                     linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
                     {
                        union(){
                           union(){
                              translate( [ 1.000000, 1.000000 ] ){
                              }
                           }translate( [ 3.000000, 3.000000 ] ){
                              resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                              }
                           }
                        }
                     }
                  }
               }
            }
            translate( [ 1.000000, 3.000000, 3.000000 ] ){
               rotate( [ 0.000000, -90.000000, 0.000000 ] ){
                  linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
                  {
                     union(){
                        union(){
                           translate( [ 1.000000, 1.000000 ] ){
                           }
                        }translate( [ 3.000000, 3.000000 ] ){
                           union(){
                              translate( [ 0.000000, 13.500000, 0.000000 ] ){
                                 resize( [ 23.000000, 9.500000 ], auto=[false, false, true] ){
                                 }
                              }resize( [ 23.000000, 9.500000 ], auto=[false, false, true] ){
                              }
                           }
                        }
                     }
                  }
               }
            }
         }
         translate( [ 3.000000, 1.000000, 3.000000 ] ){
            rotate( [ 90.000000, 0.000000, 0.000000 ] ){
               linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
               {
                  union(){
                     union(){
                        translate( [ 1.000000, 1.000000 ] ){
                        }
                     }translate( [ 3.000000, 3.000000 ] ){
                        resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                        }
                     }
                  }
               }
            }
         }
      }
      translate( [ 3.000000, 3.000000, 34.000000 ] ){
         linear_extrude( height=1.000000, twist=0.000000, scale=1.000000, $fn=32 )
         {
            union(){
               union(){
                  translate( [ 1.000000, 1.000000 ] ){
                  }
               }translate( [ 3.000000, 3.000000 ] ){
                  resize( [ 23.000000, 23.000000 ], auto=[false, false, true] ){
                  }
               }
            }
         }
      }
   }
}